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
model_path = os.path.join('model', 'cinnamon-model.h5')
model = tf.keras.models.load_model(model_path)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Class names
class_names = ["healthy_cinnamon", "leaf_spot_disease", "rough_bark", "stripe_canker"]


import numpy as np
import tensorflow as tf
import cv2
import logging
from tensorflow.keras.preprocessing.image import load_img, img_to_array

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
        # Find the last convolutional layer dynamically
        last_conv_layer = [layer for layer in model.layers if 'conv' in layer.name][-1]

        if last_conv_layer is None:
            raise ValueError("Last convolutional layer not found.")

        # Create a model that outputs the last conv layer and predictions
        grad_model = tf.keras.models.Model(
            [model.input], [last_conv_layer.output, model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, class_index]  # Target class loss

        # Compute gradients of the target class with respect to feature maps
        grads = tape.gradient(loss, conv_outputs)

        # Apply HiRes-CAM formula: Multiply gradients with the feature maps directly
        heatmap = conv_outputs * grads

        # Ensure non-negative attributions
        heatmap = np.maximum(heatmap, 0)

        # Compute mean over feature maps
        heatmap = np.mean(heatmap, axis=-1)[0]

        # Normalize heatmap
        heatmap = heatmap / (np.max(heatmap) + 1e-8)

        # Resize heatmap to input size
        heatmap = cv2.resize(heatmap, (224, 224))

        logging.debug("HiRes-CAM heatmap generated successfully.")
        return heatmap

    except Exception as e:
        logging.error(f"Error in HiRes-CAM: {str(e)}")
        raise



from tf_explain.core.grad_cam import GradCAM

def get_last_conv_layer(model):
    """Find the last convolutional layer of the model."""
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    raise ValueError("No Conv2D layer found in the model.")

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join('static', file.filename)
        file.save(file_path)
        img, img_array = preprocess_image(file_path)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        # Check cam_type (default to HiRes-CAM)
        cam_type = request.args.get("cam_type", "hirescam")

        if cam_type == "gradcam":
            last_conv_layer_name = get_last_conv_layer(model)
            explainer = GradCAM()
            heatmap = explainer.explain(
                validation_data=(img_array, None),
                model=model,
                class_index=predicted_class,
                layer_name=last_conv_layer_name  # Ensure it targets the last Conv2D layer
            )
        else:
            heatmap = hires_cam(model, img_array, predicted_class)

        # Overlay heatmap on image
        img = Image.open(file_path).convert("RGB")
        original_image = np.array(img)
        original_image = cv2.resize(original_image, (224, 224))

        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        superimposed_image = cv2.addWeighted(heatmap, 0.5, original_image, 1 - 0.5, 0)

        # Add class label
        label = class_names[predicted_class]
        cv2.putText(
            superimposed_image, label, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )

        # Convert to base64
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
