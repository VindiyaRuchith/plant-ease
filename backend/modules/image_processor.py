import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_path, target_size=(224, 224)):
        """Preprocess the uploaded image."""
        try:
            img = load_img(image_path, target_size=target_size)
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0  # Normalize to [0, 1]
            return img, img_array
        except Exception as e:
            raise ValueError(f"Error preprocessing image {image_path}: {str(e)}")
