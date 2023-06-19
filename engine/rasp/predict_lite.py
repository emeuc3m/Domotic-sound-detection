# Run manually to verify correct installation in raspberry pi

from tflite_runtime.interpreter import Interpreter
import numpy as np
from utils import get_mfccs_from_file

TEST_PATH = "./test_data/test.wav"
INT_TO_CLASS = {0: "Noise", 1: "Doorbell"}

interpreter = Interpreter(model_path="./model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

x = get_mfccs_from_file(TEST_PATH)
x = np.array([x], dtype=np.float32)
x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
input_data = np.expand_dims(x[0], axis=0)

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])

print(INT_TO_CLASS[np.argmax(output_data)])