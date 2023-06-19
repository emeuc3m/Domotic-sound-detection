# To be executed in windows systems, uses tensorflow

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import signal
import sys
import time
import pyaudio
import numpy as np
import tensorflow.keras.models as models
from utils import get_mfcc, post_alert

DEBUG = True
CLIP_LENGTH = 3
CHUNK = 22050*CLIP_LENGTH
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 22050
MODEL = "./windows/model.h5"
INT_TO_CLASS = {0: "Noise", 1: "Doorbell"}

def record_window():
    return stream.read(CHUNK)

def predict(mfcc):
    x = np.array([mfcc])
    x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
    data = np.expand_dims(x[0], axis=0)
    pred = model(data)
    return INT_TO_CLASS[np.argmax(pred)]

def terminate(sig, frame):
    print("SIGINT detected, stopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    if DEBUG:
        for i in range(p.get_device_count()):
            print(p.get_device_info_by_index(i))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)

    signal.signal(signal.SIGINT, terminate)
    model = models.load_model(MODEL)

    print("Empezando: ")
    while True:
        data = record_window()
        if DEBUG:
            stream.write(data, CHUNK)
        np_data = np.frombuffer(data, dtype=np.float32)
        start = time.time()
        mfccs = get_mfcc(np_data)
        prediction = predict(mfccs)
        if prediction != "Noise":
            post_alert(prediction)
        end = time.time()
        print(f"{prediction} (in: {end-start}s)")