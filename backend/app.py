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

MODEL_URL = "https://drive.google.com/uc?id=1XJDKqFv7Tudzvqg3ZlNqCmWDpMlUSd2M"
MODEL_LOCAL_PATH = os.path.join(os.getcwd(), 'model.h5')

# Download the model if not done already
if not os.path.exists(MODEL_LOCAL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_LOCAL_PATH, quiet=False)

# --- Flask Setup ---
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

model_handler = ModelHandler(MODEL_LOCAL_PATH)
xai_handler = XAIHandler(model_handler.model)
class_names = ["healthy cinnamon", "leaf spot disease", "rough bark", "stripe canker"]

@app.route('/')
def index():
    return "Flask backend is running"

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save uploaded file
        file_path = os.path.join('static', file.filename)
        file.save(file_path)

        # Preprocess & predict
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

        return jsonify({
            'prediction': class_names[predicted_class],
            'cam_path': img_str
        })

    except Exception as e:
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#    app.run()