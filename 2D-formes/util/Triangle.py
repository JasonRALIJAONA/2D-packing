import math
import random

class Triangle:
    def __init__(self,id ,base):
        self.id = id
        self.width = base
        self.height = (math.sqrt(3) / 2) * base
        self.pos_x = -1
        self.pos_y = -1
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


    def __init__(self, id, base, pos_x=-1, pos_y=-1, color=(0, 0, 0), **kwargs):
        self.id = id
        self.width = base
        self.height = base
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))