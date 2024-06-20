import os
import pickle
from converter import createWaveFileFromPath

path= r"D:\Find similar vocal\project\songs"
file_names = os.listdir(path)
wavefiles = []
for f in file_names:
    obj = createWaveFileFromPath(path + "/" + f)
    obj.show()
    wavefiles.append(obj)

    
with open('list_wavefile.obj', 'wb') as output:
    pickle.dump(wavefiles, output, pickle.HIGHEST_PROTOCOL)

    