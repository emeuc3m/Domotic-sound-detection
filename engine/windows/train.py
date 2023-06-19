import random
import numpy as np
import tensorflow as tf
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from utils import \
    get_files_from_folder, \
    get_mfccs_from_files
from model_conversor import convert_model


MFCC_IMAGES_PATH = "./windows/data/mfcc_images/"
DOORBELL_PATH = "./windows/data/doorbell_dataset"
NOISE_PATH = "./windows/data/noise_dataset"

TFLITE_MODEL_PATH = "./rasp/model.tflite"
MODEL_PATH = "./windows/model.h5"

CPKT = "./windows/cpkt/"

doorbell_files = get_files_from_folder(DOORBELL_PATH)
noise_files = get_files_from_folder(NOISE_PATH)

# Datasets are of the form: [(mfcc, tag)] where:
#   - mfcc is a np.array with the 2D image of the coefficients extracted
#   - tag is the number representing the class of the audio (1: doorbell, 0: noise) 
doorbell_dataset = get_mfccs_from_files(doorbell_files, 1)
noise_dataset = get_mfccs_from_files(noise_files, 0)
# Load the dataset and randomize it's order
dataset = doorbell_dataset+noise_dataset
random.shuffle(dataset)
x, y = [], []
for ii in range(len(dataset)):
    x.append(dataset[ii][0])
    y.append(dataset[ii][1])

x = np.array(x)
y = np.array(y)
# Reshape the data to the necessary shape
y = tf.keras.utils.to_categorical(y , num_classes=2)
x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
# Split in train and validation sets. 
# validation set is only 20% since there isn't much data to work with.
x_train , x_val , y_train , y_val = train_test_split(x , y ,test_size=0.2, random_state=2023)

INPUT_SHAPE = (13,130,1)
NUM_CLASSES=2
# Build the CNN
model =  models.Sequential([
                          layers.Conv2D(16 , (3,3),activation = 'relu',padding='valid', input_shape = INPUT_SHAPE),
                          layers.Conv2D(16, (3,3), activation='relu',padding='valid'),

                          layers.Conv2D(32, (3,3), activation='relu',padding='valid'),
                          layers.Conv2D(64, (3,3), activation='relu',padding='valid'),

                          layers.Conv2D(128, (3,3), activation='relu',padding='valid'),
                          layers.Conv2D(256, (3,3), activation='relu',padding='valid'),

                          layers.GlobalAveragePooling2D(),


                          layers.Dense(1024 , activation = 'relu'),
                          layers.Dense(1024 , activation = 'relu'),
    
                          layers.Dense(NUM_CLASSES , activation = 'softmax')
])
# Since there's many more examples of noise, 
# adjust the class weights to take into account more the doorbells.
class_weights = {
    0: 1.0,
    1: 36/17
}
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = 'acc')

model.summary()

# To prevent overfitting
callback_1 = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto',
    baseline=None, restore_best_weights=False
)

# To save the best possible model
callback_2 = tf.keras.callbacks.ModelCheckpoint(
    CPKT, monitor='val_loss', verbose=0, save_best_only=True,
    save_weights_only=True, mode='auto', save_freq='epoch', options=None
)

# Train the model
history = model.fit(x_train,y_train ,
            validation_data=(x_val,y_val),
            class_weight=class_weights,
            epochs=50)
# Save it as .h5
model.save(MODEL_PATH)
# Save it as .tflite
convert_model(MODEL_PATH, TFLITE_MODEL_PATH)

# Print the confusion matrix
print(y_val)
y_pred = np.argmax(model.predict(x_val),axis=1)
print('Confusion Matrix')
confusionMatrix = confusion_matrix(y_pred, np.argmax(y_val,axis=1))
print(confusionMatrix)