import tensorflow as tf

def convert_model(h5_path: str, path: str):
    model = tf.keras.models.load_model(h5_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open(path, "wb").write(tflite_model)

if __name__ == '__main__':
    DEFAULT_H5_PATH = "./windows/model.h5"
    DEFAULT_TFLITE_NAME = "./rasp/test.tflite"

    convert_model(DEFAULT_H5_PATH, DEFAULT_TFLITE_NAME)