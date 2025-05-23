# Import necessary libraries
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.metrics import AUC, Precision, Recall
import os
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

# Paths 

# Paths to training and validation CSV files and image directories
train_csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train\_classes.csv'
train_image_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train'

val_csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\valid\_classes.csv'
val_image_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\valid'

# Load CSVs

# Load CSV files containing filenames and labels
df_train = pd.read_csv(train_csv_path)
df_val = pd.read_csv(val_csv_path)

# Add full image paths to the dataframe for use in generators
df_train['image_path'] = df_train['filename'].apply(lambda x: os.path.join(train_image_path, x))
df_val['image_path'] = df_val['filename'].apply(lambda x: os.path.join(val_image_path, x))

# Image Parameters 
# Resize all images to this size
IMG_SIZE = (224, 224)
# Number of images processed in one batch
BATCH_SIZE = 32         

# Image Augmentation

# Training data preprocessing and augmentation to improve generalization
train_datagen = ImageDataGenerator(
    # Normalize pixel values to [0,1]
    rescale=1./255,
    # Random rotation
    rotation_range=20,
    # Random brightness
    brightness_range=[0.8, 1.2],
    # Random zoom
    zoom_range=0.1,
    # Random horizontal flip
    horizontal_flip=True,
    # Fill pixels when rotating or shifting
    fill_mode='nearest'          
)

# Validation data is only normalized
val_datagen = ImageDataGenerator(rescale=1./255)

# Data Generators 

# Train generator that reads images and corresponding labels
train_generator = train_datagen.flow_from_dataframe(
    dataframe=df_train,
    x_col='image_path',
    # One-hot encoded columns
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],  
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    # For multi-class with one-hot
    class_mode='raw',
    # Shuffling the data during training
    shuffle=True       
)

# Validation generator
val_generator = val_datagen.flow_from_dataframe(
    dataframe=df_val,
    x_col='image_path',
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',
    # Not shuffling during validation
    shuffle=False      
)

#  Model Definition 

# Input layer for 224x224 RGB images
input_layer = Input(shape=(224, 224, 3))

# Convolutional & Pooling layers
x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(128, (3, 3), activation='relu')(x)
x = MaxPooling2D((2, 2))(x)

# Flatten feature maps into a vector
x = Flatten()(x)

# Dense hidden layer
x = Dense(128, activation='relu')(x)
# Dropout for regularization
x = Dropout(0.5)(x)  

# Output layer with softmax for 4-class classification
output_layer = Dense(4, activation='softmax')(x)

# Create the model
model = Model(inputs=input_layer, outputs=output_layer)

# Compile the Model

# Use=ing categorical_crossentropy for multi-class one-hot targets
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy', Precision(), Recall(), AUC(name='auc')]
)

# Train the Model 

# Train the model and save training history
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    verbose=1
)

# Save the Model
model.save(r"C:\Users\Vindiya\Desktop\DEPLOY\backend\performancemodel.keras")
