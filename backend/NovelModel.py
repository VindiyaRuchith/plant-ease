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
train_csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train\_classes.csv'
train_image_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train'

val_csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\valid\_classes.csv'
val_image_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\valid'

# Load CSVs
df_train = pd.read_csv(train_csv_path)
df_val = pd.read_csv(val_csv_path)

# Add full image paths
df_train['image_path'] = df_train['filename'].apply(lambda x: os.path.join(train_image_path, x))
df_val['image_path'] = df_val['filename'].apply(lambda x: os.path.join(val_image_path, x))

# Image parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    brightness_range=[0.8, 1.2],
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# No augmentation for validation
val_datagen = ImageDataGenerator(rescale=1./255)

# Data generators 
train_generator = train_datagen.flow_from_dataframe(
    dataframe=df_train,
    x_col='image_path',
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',  # one-hot labels
    shuffle=True
)

val_generator = val_datagen.flow_from_dataframe(
    dataframe=df_val,
    x_col='image_path',
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',
    shuffle=False
)

# Model definition
input_layer = Input(shape=(224, 224, 3))
x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
x = MaxPooling2D((2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output_layer = Dense(4, activation='softmax')(x)  # softmax for multi-class

model = Model(inputs=input_layer, outputs=output_layer)

# Compile with appropriate loss
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',  # for one-hot multi-class
    metrics=['accuracy', Precision(), Recall(), AUC(name='auc')]
)

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    verbose=1
)

# Save model
model.save(r"C:\Users\Vindiya\Desktop\model_multiclass.h5")