# Import necessary libraries
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class ImageProcessor:
    @staticmethod
    # Preprocess the uploaded image for model prediction
    def preprocess_image(image_path, target_size=(224, 224)):
        try:
            # Load the image and resize it to the target size
            img = load_img(image_path, target_size=target_size)
            
            # Convert the image to a NumPy array (height, width, channels)
            img_array = img_to_array(img)
            
            # Add a batch dimension (1, height, width, channels)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Normalize pixel values to the range [0, 1]
            img_array /= 255.0
            
            # Return the original image and the preprocessed array
            return img, img_array
        
        except Exception as e:
            # Raise a meaningful error if anything goes wrong during preprocessing
            raise ValueError(f"Error preprocessing image {image_path}: {str(e)}")
