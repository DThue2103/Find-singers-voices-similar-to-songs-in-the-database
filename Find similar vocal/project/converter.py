import librosa
import numpy as np
from wavefile import WaveFile
import pickle

def normalize(vector):
    with open('normalize.obj', 'rb') as input:
        min_arr = pickle.load(input)
        max_arr = pickle.load(input)
        vector = np.array(vector)
    return (vector-min_arr) / (max_arr-min_arr)

def average_energy(arr):
    return np.average(arr*arr)

def createWaveFileFromPath(path):

    x,sr = librosa.load(path)
    ave_energy = average_energy(x)
    spec_cent = librosa.feature.spectral_centroid(y=x, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=x, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=x, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(x)
    feature_vector = [ave_energy, np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    
    feature_vector = normalize(feature_vector)
    
    obj = WaveFile(feature_vector, path)
    return obj   
    
