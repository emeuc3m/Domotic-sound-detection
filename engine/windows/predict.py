import random
import time
import numpy as np
import tensorflow as tf
import tensorflow.keras.models as models

from utils import \
    get_files_from_folder, \
    get_mfccs_from_files, \
    get_mfccs_from_file

pred_to_class = {0: "Noise", 1: "Doorbell"}
DOORBELL_PATH = "./windows/data/doorbell_dataset"
NOISE_PATH = "./windows/data/noise_dataset"
path = "./windows/data/test.wav"

doorbell_files = get_files_from_folder(DOORBELL_PATH)
noise_files = get_files_from_folder(NOISE_PATH)

# Datasets are of the form: [(mfcc, tag)] where:
#   - mfcc is a np.array with the 2D image of the coefficients extracted
#   - tag is the number representing the class of the audio (1: doorbell, 0: noise) 
doorbell_dataset = get_mfccs_from_files(doorbell_files, 1)
noise_dataset = get_mfccs_from_files(noise_files, 0)

dataset = doorbell_dataset+noise_dataset
random.shuffle(dataset)
x, y = [], []
for ii in range(len(dataset)):
    x.append(dataset[ii][0])

model = models.load_model("./model.h5")

start = time.time()
x = get_mfccs_from_file(path)
end = time.time()
x = np.array([x])
x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
print("MFCCs time: ", end-start)


test = np.expand_dims(x[0], axis=0)
start = time.time()
t = model(test)
prediction = pred_to_class[np.argmax(t)]
end = time.time()
print("Prediction: \n\t", prediction, "\n\t", t, "\n time: ", end-start)