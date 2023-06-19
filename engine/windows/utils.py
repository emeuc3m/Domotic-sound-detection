import os
import time
import requests
from librosa import load as lib_load
from librosa.feature import mfcc as lib_mfcc
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm


def get_mfcc(data, sr=22050):
    mfccs = lib_mfcc(y=data, sr=sr, n_mfcc=13, dct_type=3)
    return mfccs

def get_mfccs_from_file(file: str) -> "list[tuple]":
    signal, sample_rate = lib_load(file)
    return lib_mfcc(y=signal, n_mfcc=13, dct_type=3)
    

def get_mfccs_from_files(files: "list[str]", tag: int) -> "list[tuple]":
    dataset = []
    for file in files:
        mfcc = get_mfccs_from_file(file)
        dataset.append((mfcc, tag))
    return dataset

def get_files_from_folder(folder_name: str) -> "list[str]":
    files = []
    for file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def post_alert(type: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'type': type,
        'timestamp': int(time.time()),
    }

    return requests.post('http://127.0.0.1:8000/alerts', headers=headers, json=json_data)

# def plot_mfcc(mfcc, savefig: bool=False, file: str = "default.png") -> None:

#     fig, ax = plt.subplots()
#     mfcc= np.swapaxes(mfcc, 0 ,1)
#     cax = ax.imshow(mfcc, interpolation='nearest', cmap=cm.coolwarm, origin='lower')
#     ax.set_title('MFCC')

#     if savefig:
#         plt.savefig(file)
#     else:
#         plt.show()
#     plt.close(fig)

# def save_mfccs_fig(dataset: "list[tuple]", path: str = "", filename: str = "default.png") -> None:
#     for ii, mfcc  in enumerate(dataset):
#         plot_mfcc(mfcc[0], file=f"{path}{ii}-{filename}", savefig=True)
