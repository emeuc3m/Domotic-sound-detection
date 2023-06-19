# To be executed in linux systems, uses tflite_runtime.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import signal
import sys
import time
import pyaudio
import numpy as np
from tflite_runtime.interpreter import Interpreter
from utils import get_mfcc, post_alert

DEBUG = True
LISTEN_STREAM = False
CLIP_LENGTH = 3
CHUNK = 22050*CLIP_LENGTH
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 22050
MODEL = "./model.tflite"
INT_TO_CLASS = {0: "Noise", 1: "Doorbell"}

def record_window():
    return stream.read(CHUNK)

def predict(mfcc):
    x = get_mfcc(mfcc)
    x = np.array([x], dtype=np.float32)
    x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
    input_data = np.expand_dims(x[0], axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    return INT_TO_CLASS[np.argmax(output_data)]

def terminate(sig, frame):
    print("Terminando")
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

    interpreter = Interpreter(model_path=MODEL)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']

    print("Empezando: ")
    while True:
        data = record_window()
        if LISTEN_STREAM:
            stream.write(data, CHUNK)
        np_data = np.frombuffer(data, dtype=np.float32)
        start = time.time()
        mfccs = get_mfcc(np_data)
        prediction = predict(mfccs)
        if prediction != "Noise":
            post_alert(prediction)
        end = time.time()
        print(f"{prediction} (in: {end-start}s)")



