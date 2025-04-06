import numpy as np
import tensorflow as tf
import cv2

class XAIHandler:
    def __init__(self, model):
        # Store the model for use in both explanation methods
        self.model = model

    def hires_cam(self, img_array, class_index):
        ## Generate a heatmap using HiRes-CAM (High-Resolution CAM).
        ## Uses element-wise multiplication of gradients and feature maps,
        ## followed by summation across channels.
        try:
            # Get the last convolutional layer from the model
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]

            # Create a model that outputs both feature maps and predictions
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            # Record operations for gradient computation
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, class_index]  # Focus on the output neuron of the target class

            # Compute gradients of the target class with respect to feature maps
            grads = tape.gradient(loss, conv_outputs)

            # Multiply feature maps with gradients (element-wise)
            heatmap = conv_outputs * grads
            heatmap = np.maximum(heatmap, 0)  # Apply ReLU (zero out negative values)

            # Sum across channels to get the final heatmap
            heatmap = np.sum(heatmap, axis=-1)[0]

            # Normalize the heatmap to [0, 1]
            heatmap /= np.max(heatmap) + 1e-8

            # Resize heatmap to match input image size
            heatmap = cv2.resize(heatmap, (224, 224))
            return heatmap

        except Exception as e:
            raise ValueError(f"Error in HiRes-CAM: {str(e)}")

    def grad_cam_plus(self, img_array, class_index):
        """
        Generate a heatmap using Grad-CAM++.
        Uses higher-order derivatives to improve localization compared to basic Grad-CAM.
        """
        try:
            # Get the last convolutional layer from the model
            last_conv_layer = [layer for layer in self.model.layers if 'conv' in layer.name][-1]

            # Create a model that outputs both feature maps and predictions
            grad_model = tf.keras.models.Model([self.model.input], [last_conv_layer.output, self.model.output])

            # Record gradient computations at different levels
            with tf.GradientTape(persistent=True) as tape1:
                with tf.GradientTape(persistent=True) as tape2:
                    with tf.GradientTape() as tape3:
                        conv_outputs, predictions = grad_model(img_array)
                        loss = predictions[:, class_index]  # Focus on target class

                    # First-order gradient
                    grads = tape3.gradient(loss, conv_outputs)

                # First derivative of output with respect to conv layer
                first_derivative = tape2.gradient(loss, conv_outputs)

            # Second derivative of output with respect to conv layer
            second_derivative = tape1.gradient(first_derivative, conv_outputs)

            # Remove batch dimension
            conv_outputs = conv_outputs[0]
            grads = grads[0]
            first_derivative = first_derivative[0]
            second_derivative = second_derivative[0]

            # Compute alpha weights for Grad-CAM++ (element-wise importance)
            numerator = second_derivative
            denominator = 2.0 * second_derivative + tf.square(grads)
            # Avoid division by zero
            denominator = tf.where(denominator != 0.0, denominator, tf.ones_like(denominator))

            # Calculate alpha values
            alphas = numerator / denominator
            # Replace NaNs with zeros
            alphas = tf.where(tf.math.is_nan(alphas), tf.zeros_like(alphas), alphas)

            # Calculate weights by combining alphas and positive gradients
            weights = tf.reduce_sum(alphas * tf.nn.relu(grads), axis=(0, 1))

            # Weighted combination of conv feature maps
            cam = tf.reduce_sum(weights * conv_outputs, axis=-1)

            # Apply ReLU and normalize CAM
            cam = tf.nn.relu(cam)
            cam = cam - tf.reduce_min(cam)
            cam = cam / (tf.reduce_max(cam) + 1e-8)

            # Resize heatmap to match input image size
            heatmap = tf.image.resize(cam[..., tf.newaxis], (224, 224)).numpy().squeeze()

            return heatmap

        except Exception as e:
            raise ValueError(f"Error in Grad-CAM++: {str(e)}")

