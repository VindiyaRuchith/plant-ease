import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.model_handler import ModelHandler
from modules.image_processor import ImageProcessor
from modules.xai_handler import XAIHandler
from modules.utils import Utils

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Load model
MODEL_PATH = os.path.join('model', 'novel-model.h5')
model_handler = ModelHandler(MODEL_PATH)
xai_handler = XAIHandler(model_handler.model)

# Class names
class_names = ["healthy_cinnamon", "leaf_spot_disease", "rough_bark", "stripe_canker"]

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

        if confidence < 0.8:
            return jsonify({"error": "The image does not appear to be a cinnamon leaf."}), 400

        heatmap = xai_handler.hires_cam(img_array, predicted_class)
        img_str = Utils.overlay_heatmap(file_path, heatmap, confidence)

        return jsonify({
            'confidence': round(confidence * 100, 2),
            'prediction': class_names[predicted_class],
            'cam_path': img_str
        })

    except Exception as e:
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
