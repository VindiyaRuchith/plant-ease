import numpy as np
import tensorflow as tf
import cv2


class XAIHandler:
    def __init__(self, model):
        self.model = model

    def hires_cam(self, img_array, class_index):
        """Generate a heatmap using HiRes-CAM."""
        try:
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, class_index]

            grads = tape.gradient(loss, conv_outputs)[0]  # Remove batch
            conv_outputs = conv_outputs[0]  # Remove batch

            # HiRes-CAM: Multiply conv outputs with gradients element-wise
            heatmap = conv_outputs * grads
            heatmap = np.maximum(heatmap, 0)
            heatmap = np.sum(heatmap, axis=-1)
            heatmap /= np.max(heatmap) + 1e-8
            heatmap = cv2.resize(heatmap, (224, 224))

            return heatmap

        except Exception as e:
            raise ValueError(f"Error in HiRes-CAM: {str(e)}")

    def grad_cam_plus(self, img_array, class_index):
        """Generate a heatmap using Grad-CAM++."""
        try:
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            with tf.GradientTape(persistent=True) as tape1:
                with tf.GradientTape(persistent=True) as tape2:
                    with tf.GradientTape() as tape3:
                        conv_outputs, predictions = grad_model(img_array)
                        loss = predictions[:, class_index]

                    grads = tape3.gradient(loss, conv_outputs)
                first_derivative = tape2.gradient(loss, conv_outputs)
            second_derivative = tape1.gradient(first_derivative, conv_outputs)

            conv_outputs = conv_outputs[0]
            grads = grads[0]
            first_derivative = first_derivative[0]
            second_derivative = second_derivative[0]

            # Alpha computation
            numerator = second_derivative
            denominator = 2.0 * second_derivative + tf.square(grads)
            denominator = tf.where(denominator != 0.0, denominator, tf.ones_like(denominator))
            alphas = numerator / denominator
            alphas = tf.where(tf.math.is_nan(alphas), tf.zeros_like(alphas), alphas)

            weights = tf.reduce_sum(alphas * tf.nn.relu(grads), axis=(0, 1))
            cam = tf.reduce_sum(weights * conv_outputs, axis=-1)

            cam = tf.nn.relu(cam)
            cam = cam - tf.reduce_min(cam)
            cam = cam / (tf.reduce_max(cam) + 1e-8)

            heatmap = tf.image.resize(cam[..., tf.newaxis], (224, 224)).numpy().squeeze()

            return heatmap

        except Exception as e:
            raise ValueError(f"Error in Grad-CAM++: {str(e)}")
