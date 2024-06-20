
import pickle

with open('list_wavefile.obj', 'rb') as input:
    wavefiles = pickle.load(input)
    for item in wavefiles: print('{}'.format(item.features), end='')