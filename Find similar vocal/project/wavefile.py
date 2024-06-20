from typing import List

class WaveFile:
    def __init__(self, features: List, location: str):
        self.features = features
        self.location = location
    def show(self):
        print(self.features)
        print(self.location)
    