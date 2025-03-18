import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.model_handler import ModelHandler
from modules.image_processor import ImageProcessor
from modules.xai_handler import XAIHandler
from modules.utils import Utils
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Cloud Storage Configuration
BUCKET_NAME = "plantease-bucket"  # Replace with your bucket name
BLOB_NAME = "novel-model-upgraded.keras"  # Replace with your model file name

# Load credentials from environment variable
credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
credentials_info = json.loads(credentials_json)

# Local Model Path
MODEL_PATH = "novel-model-upgraded.keras"

# Load model
model_handler = ModelHandler(MODEL_PATH, BUCKET_NAME, BLOB_NAME, credentials_info)
xai_handler = XAIHandler(model_handler.model)

# Class names
class_names = ["healthy cinnamon", "leaf spot disease", "rough bark", "stripe canker"]

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join('static', file.filename)
        file.save(file_path)
        img, img_array = ImageProcessor.preprocess_image(file_path)

        predictions = model_handler.predict(img_array)
        predicted_class = predictions.argmax()
        confidence = float(predictions[0][predicted_class])

        if confidence < 0.7:
            return jsonify({"error": "The image does not appear to be a cinnamon leaf."}), 400

        heatmap = xai_handler.hires_cam(img_array, predicted_class)
        img_str = Utils.overlay_heatmap(file_path, heatmap, confidence)

        return jsonify({
            'prediction': class_names[predicted_class],
            'cam_path': img_str
        })

    except Exception as e:
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
