import pickle
from sys import argv
from backend_tree import KDTree
from converter import createWaveFileFromPath
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

#Load the premade tree
with open('premade_tree.obj', 'rb') as input:
    tree = pickle.load(input)

print("-----------Xin hãy chọn bài hát-----------")
file_path = filedialog.askopenfilename()
if file_path:
    obj = createWaveFileFromPath(file_path)
    print('Bài hát được chọn: ', end='')
    print(obj.location)
    #print(obj.features)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("3 files âm thanh giống nhất:")
       
    output_list = tree.k_search(obj)
    for data_found, distance in output_list:
        if data_found is not None:  
            print(data_found.data.location, distance)