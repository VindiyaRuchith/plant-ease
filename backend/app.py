import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
from PIL import Image
from io import BytesIO
import base64
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load and compile the model
model_path = os.path.join('model', 'cinnamon_model.h5')
model = tf.keras.models.load_model(model_path)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Class names
class_names = ["healthy_cinnamon", "leaf_spot_disease", "rough_bark", "stripe_canker"]


def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess the uploaded image."""
    try:
        img = load_img(image_path, target_size=target_size)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize to [0, 1]
        logging.debug(f"Image preprocessed successfully: {image_path}")
        return img, img_array
    except Exception as e:
        logging.error(f"Error preprocessing image {image_path}: {str(e)}")
        raise


def hires_cam(model, img_array, class_index):
    """Generate a heatmap using HiRes-CAM."""
    try:
        # Identify the last convolutional layer
        last_conv_layer = model.get_layer("conv2d_3")
        if last_conv_layer is None:
            raise ValueError("Last convolutional layer not found.")

        # Create a model that outputs the last conv layer and predictions
        grad_model = tf.keras.models.Model(
            [model.inputs], [last_conv_layer.output, model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, class_index]  # Target class loss

        # Compute gradients of the target class with respect to feature maps
        grads = tape.gradient(loss, conv_outputs)

        # HiRes-CAM: Clip to positive gradients
        grads = tf.nn.relu(grads)

        # HiRes-CAM: Compute pixel-wise attribution
        heatmap = grads * conv_outputs
        heatmap = np.maximum(heatmap, 0)  # ReLU to ensure non-negative
        heatmap = np.mean(heatmap, axis=-1)[0]  # Combine channel contributions

        # Normalize heatmap to [0, 1]
        heatmap = heatmap / (np.max(heatmap) + 1e-8)

        # Resize heatmap to input size
        heatmap = cv2.resize(heatmap, (224, 224))

        logging.debug("HiRes-CAM heatmap generated successfully.")
        return heatmap
    except Exception as e:
        logging.error(f"Error in HiRes-CAM: {str(e)}")
        raise


@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save and preprocess the image
        file_path = os.path.join('static', file.filename)
        file.save(file_path)
        img, img_array = preprocess_image(file_path)

        # Predict the class probabilities
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        # Generate HiRes-CAM heatmap
        heatmap = hires_cam(model, img_array, predicted_class)

        # Load the original image as RGB
        img = Image.open(file_path).convert("RGB")
        original_image = np.array(img)
        original_image = cv2.resize(original_image, (224, 224))

        # Overlay the heatmap on the original image
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Blend the heatmap with the original image
        alpha = 0.5  # Transparency for the heatmap
        superimposed_image = cv2.addWeighted(heatmap, alpha, original_image, 1 - alpha, 0)

        # Add the class label to the image
        label = class_names[predicted_class]
        cv2.putText(
            superimposed_image, label, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )

        # Convert the image to base64 for return
        img_pil = Image.fromarray(cv2.cvtColor(superimposed_image, cv2.COLOR_BGR2RGB))
        buffered = BytesIO()
        img_pil.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({'prediction': label, 'cam_path': img_str})

    except Exception as e:
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": f"Error during classification: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
