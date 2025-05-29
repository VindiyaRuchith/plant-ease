# Import the libraries
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# module imports
# Handles model loading and predictions
from modules.model_handler import ModelHandler
# Handles image preprocessing
from modules.image_processor import ImageProcessor
# Generates Grad-CAM++ or HiRes-CAM
from modules.xai_handler import XAIHandler
# Utilities for overlaying heatmap
from modules.image_overlay import ImageOverlay                     

MODEL_LOCAL_PATH = os.path.join(os.path.dirname(__file__), 'model.h5')

# Flask Setup
app = Flask(__name__)
# Enable CORS to allow cross-origin requests from frontend
CORS(app)
# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Load Model and Handlers 
# Loads the trained model
model_handler = ModelHandler(MODEL_LOCAL_PATH)
# Pass the model to XAI handler
xai_handler = XAIHandler(model_handler.model)
# Class labels
class_names = ["healthy cinnamon", "leaf spot disease", "rough bark", "stripe canker"]

# Routes

@app.route('/')
def index():
    # route to check if the backend is running
    return "Flask backend is running"

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        # File Validation 
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save Uploaded Image 
        file_path = os.path.join('static', file.filename)
        file.save(file_path)

        # Preprocess Image & Predict Class
        # Resize, normalize, etc.
        img_array = ImageProcessor.preprocess_image(file_path)
        # Get predictions
        predictions = model_handler.predict(img_array)
        # Index of highest probability
        predicted_class = predictions.argmax()
         # Confidence score
        confidence = float(predictions[0][predicted_class])         

        # Confidence Threshold Check
        if confidence < 0.45:
            return jsonify({
                "error": "Sorry we're having trouble identifying this image. Please reduce background as much as possible"
            }), 400

        # Determine Which CAM Method to Use
        # Optional query parameter to specify CAM type (default is 'hires')
        cam_type = request.args.get('cam_type', 'hires')  

        # Generate the appropriate heatmap
        if cam_type == "gradcam":
            heatmap = xai_handler.grad_cam_plus(img_array, predicted_class)
        else:
            heatmap = xai_handler.hires_cam(img_array, predicted_class)

        # Overlay Heatmap on Original Image
        img_str = ImageOverlay.overlay_heatmap(file_path, heatmap, confidence)

        # Return Prediction and Heatmap Path 
        return jsonify({
            'prediction': class_names[predicted_class],
            'cam_path': img_str
        })

    except Exception as e:
        # Log any errors that occur and return a 500 response
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run()

