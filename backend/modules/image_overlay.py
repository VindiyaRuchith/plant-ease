import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

class ImageOverlay:
    @staticmethod
    def overlay_heatmap(image_path, heatmap, confidence):
        # Open the original image and convert to RGB format
        img = Image.open(image_path).convert("RGB")

        # Convert PIL image to NumPy array
        original_image = np.array(img)

        # Resize the image to match the heatmap size
        original_image = cv2.resize(original_image, (224, 224))

        # Convert heatmap to uint8 and scale values to [0, 255]
        heatmap = np.uint8(255 * heatmap)

        # Apply the JET colormap to the heatmap for better visualization
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Blend the heatmap and the original image (alpha=0.5 for equal contribution)
        superimposed_image = cv2.addWeighted(heatmap, 0.5, original_image, 1 - 0.5, 0)

        # Convert final image to base64 and return
        return ImageOverlay.image_to_base64(superimposed_image)

    @staticmethod
    def image_to_base64(image):

        # Convert BGR (OpenCV format) to RGB (PIL format)
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Create a buffer and save image to it in PNG format
        buffered = BytesIO()
        img_pil.save(buffered, format="PNG")

        # Encode buffer content to base64 and return as string
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
