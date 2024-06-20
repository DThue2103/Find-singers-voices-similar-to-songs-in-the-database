import os
import librosa
import numpy as np
import pickle

# tinh toan gia tri min,max cho tung feature
def average_energy(arr):
    return np.average(arr*arr)

def createWaveFileFromPath(path):
    x,sr = librosa.load(path)
    ave_energy = average_energy(x)
    spec_cent = librosa.feature.spectral_centroid(y=x, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=x, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=x, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(x)
    feature_vector = [ave_energy, 
                      np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    return feature_vector

path=r"D:\Find similar vocal\project\songs"
file_names = os.listdir(path)
arr = []
for f in file_names:
    obj = createWaveFileFromPath(path + "/" + f)
    arr.append(obj)

min_arr = np.vstack(arr).min(axis=0)
max_arrr = np.vstack(arr).max(axis=0)
print("Min value: ",min_arr)
print("Max value: ",max_arrr)

with open('normalize.obj', 'wb') as output:
    pickle.dump(min_arr, output, pickle.HIGHEST_PROTOCOL)
    pickle.dump(max_arrr, output, pickle.HIGHEST_PROTOCOL)