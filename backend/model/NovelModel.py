import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
import os
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, hamming_loss


# Loading the CSV file and the Image folder
csv_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train\_classes.csv'
imagefolder_path = r'C:\Users\Vindiya\Desktop\Dataset For FYP\train'


df = pd.read_csv(csv_path)


# Providing the path to the images
df['csv_path'] = df['filename'].apply(lambda x: os.path.join(imagefolder_path, x))


labels = df[['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker']]


# Defining the Image size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

datagen = ImageDataGenerator(
    rescale=1./255,  
    validation_split=0.2  
)

train_generator = datagen.flow_from_dataframe(
    dataframe=df,
    x_col='csv_path',
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',  
    subset='training',
    shuffle=True
)

validation_generator = datagen.flow_from_dataframe(
    dataframe=df,
    x_col='csv_path',
    y_col=['healthy_cinnamon', 'leaf_spot_disease', 'rough_bark', 'stripe_canker'],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='raw',
    subset='validation',
    shuffle=False
)

# Defining the New Model

# Creating the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='sigmoid')  
])


# Compiling the model with optimizer and loss function
model.compile(
    optimizer='adam',
    loss='binary_crossentropy', 
    metrics=['accuracy']
)


result = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10,
    verbose=1
)

# Save the Model
model.save(r"C:\Users\Vindiya\Desktop\PLANT-EASE\backend\models\novel-model.h5")

# Test saved model
from tensorflow.keras.models import load_model
loaded_model = load_model(r"C:\Users\Vindiya\Desktop\PLANT-EASE\backend\models\novel-model.h5")
print(loaded_model.summary())

