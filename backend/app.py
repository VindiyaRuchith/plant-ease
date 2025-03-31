import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.model_handler import ModelHandler
from modules.image_processor import ImageProcessor
from modules.xai_handler import XAIHandler
from modules.utils import Utils
import gdown
import os

# Model download Configuration
MODEL_URL = "https://drive.google.com/uc?id=1XJDKqFv7Tudzvqg3ZlNqCmWDpMlUSd2M"
MODEL_LOCAL_PATH = os.path.join(os.getcwd(), 'model.h5')

# Download the model if not done already
if not os.path.exists(MODEL_LOCAL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_LOCAL_PATH, quiet=False)

# Flask App Initialization
app = Flask(__name__)
CORS(app) # Enable CORS for frontend-backend interaction
logging.basicConfig(level=logging.DEBUG)

# Initialize model and XAI handlers
model_handler = ModelHandler(MODEL_LOCAL_PATH) # Load the model
xai_handler = XAIHandler(model_handler.model)# Pass model to XAI handler
class_names = ["healthy cinnamon", "leaf spot disease", "rough bark", "stripe canker"]

# Test route for testing backend availability
@app.route('/')
def index():
    return "Flask backend is running"

# Image classification endpoint
@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        # Check if an image was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save uploaded file to static directory
        file_path = os.path.join('static', file.filename)
        file.save(file_path)

        # Preprocess image and convert to array for prediction
        img, img_array = ImageProcessor.preprocess_image(file_path)
        predictions = model_handler.predict(img_array)
        predicted_class = predictions.argmax()
        confidence = float(predictions[0][predicted_class])

        # Check confidence threshold
        if confidence < 0.45:
            return jsonify({"error": "The image does not appear to be a cinnamon leaf."}), 400

        # Read cam_type from query parameter (default to 'hires')
        cam_type = request.args.get('cam_type', 'hires')

        # Generate heatmap based on cam_type
        if cam_type == "gradcam":
            heatmap = xai_handler.grad_cam_plus(img_array, predicted_class)
        else:
            heatmap = xai_handler.hires_cam(img_array, predicted_class)

        # Overlay and return result
        img_str = Utils.overlay_heatmap(file_path, heatmap, confidence)

        # return JSON response with prediction and heatmap
        return jsonify({
            'prediction': class_names[predicted_class],
            'cam_path': img_str
        })

    except Exception as e:
        # Log the error and return a JSON response
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Entry point commented out for deployment usage
# if __name__ == '__main__':
#    app.run()