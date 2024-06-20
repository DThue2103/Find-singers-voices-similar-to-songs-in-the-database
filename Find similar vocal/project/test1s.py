import os
import pickle
from converter import createWaveFileFromPath

path=r"C:\Users\ASUS\Downloads\Test song"
file_names = os.listdir(path)
for f in file_names:
    obj = createWaveFileFromPath(path + "\\" + f)
    obj.show()
