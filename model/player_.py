import random

class RandomPlayer:
    def __init__(self, name):
        self.name = name


    def play(self, tiles_coords):
        return random.choice(tiles_coords)