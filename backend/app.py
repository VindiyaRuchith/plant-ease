import os
import logging
import gdown  # Ensure gdown is in your requirements.txt
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.model_handler import ModelHandler
from modules.image_processor import ImageProcessor
from modules.xai_handler import XAIHandler
from modules.utils import Utils

# ---------------------------
# STEP: Check & Download Model
# ---------------------------

# Ensure the model directory exists
MODEL_DIR = os.path.join(os.getcwd(), 'model')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Define the local path where the .h5 model will be saved
MODEL_LOCAL_PATH = os.path.join(MODEL_DIR, 'novel-model.h5')

# Check if the model file exists locally; if not, download it from Google Drive
if not os.path.exists(MODEL_LOCAL_PATH):
    print("Model file not found locally. Downloading from Google Drive...")
    # Replace 'YOUR_FILE_ID' with the actual file ID from your Google Drive shareable link
    url = 'https://drive.google.com/uc?id=1G8BdSNPw5NjuVGp3yjV1s2FFVwE6BGyP'
    gdown.download(url, MODEL_LOCAL_PATH, quiet=False)
else:
    print("Model file already exists locally. No download needed.")

# ---------------------------
# Flask App Setup
# ---------------------------
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Load model using the local .h5 file
model_handler = ModelHandler(MODEL_LOCAL_PATH)
xai_handler = XAIHandler(model_handler.model)

# Class names for predictions
class_names = ["healthy cinnamon", "leaf spot disease", "rough bark", "stripe canker"]

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the uploaded image
        file_path = os.path.join('static', file.filename)
        file.save(file_path)

        # Preprocess the image
        img, img_array = ImageProcessor.preprocess_image(file_path)

        # Get predictions from the model
        predictions = model_handler.predict(img_array)
        predicted_class = predictions.argmax()
        confidence = float(predictions[0][predicted_class])

        # Check prediction confidence
        if confidence < 0.7:
            return jsonify({"error": "The image does not appear to be a cinnamon leaf."}), 400

        # Generate the heatmap using XAI
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
