import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

class Utils:
    @staticmethod
    def overlay_heatmap(image_path, heatmap, confidence):
        """Overlay heatmap on image and add confidence text."""
        img = Image.open(image_path).convert("RGB")
        original_image = np.array(img)
        original_image = cv2.resize(original_image, (224, 224))

        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        superimposed_image = cv2.addWeighted(heatmap, 0.5, original_image, 0.5, 0)

        return Utils.image_to_base64(superimposed_image)

    @staticmethod
    def image_to_base64(image):
        """Convert image to base64 string."""
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        buffered = BytesIO()
        img_pil.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
