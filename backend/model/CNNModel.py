import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, hamming_loss
import os

# Loading the CSV file and Image folder
csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train\_classes.csv'
imagefolder_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train'

# Load CSV file
df = pd.read_csv(csv_path)

# Fix column names (remove leading/trailing spaces)
df.rename(columns=lambda x: x.strip(), inplace=True)

# Add full image path
df['csv_path'] = df['filename'].apply(lambda x: os.path.join(imagefolder_path, x))

# Labels (without spaces)
y_col = ['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker']

# Validate that all image files exist
df = df[df['csv_path'].apply(os.path.exists)]
if df.empty:
    raise ValueError("No valid image files found in the specified paths!")

# Splitting dataset into training and validation
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Define Image Size and Batch Size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data Augmentation
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Training Data Generator
train_generator = datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col='csv_path',
    y_col=y_col,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',  # Multi-label output
    shuffle=True
)

# Validation Data Generator
validation_generator = datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col='csv_path',
    y_col=y_col,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',
    shuffle=False
)

# CNN Model Architecture
input_layer = Input(shape=(224, 224, 3))

x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)

x = Flatten()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)  # Reduced dropout
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)

output_layer = Dense(4, activation='sigmoid')(x)  # Multi-label classification

model = Model(inputs=input_layer, outputs=output_layer)

# Compile the Model
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train the Model
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=50,
    verbose=1
)

# Save the Model
model.save(r"C:\Users\Vindiya\Desktop\PLANT-EASE\backend\models\cinnamon-model.h5")

# Test saved model
from tensorflow.keras.models import load_model
loaded_model = load_model(r"C:\Users\Vindiya\Desktop\PLANT-EASE\backend\models\cinnamon-model.h5")
print(loaded_model.summary())

# Model Evaluation
y_true = val_df[y_col].values  # True labels
predictions = model.predict(validation_generator)  # Predicted probabilities
y_pred = (predictions > 0.5).astype(int)  # Convert to binary labels

accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average='micro')
hamming = hamming_loss(y_true, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1-score: {f1_score:.4f}")
print(f"Hamming Loss: {hamming:.4f}")

