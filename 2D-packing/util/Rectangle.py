import random

class Rectangle:
    def __init__(self,id ,width, height):
        self.id = id
        self.width = width
        self.height = height
        self.pos_x = -1
        self.pos_y = -1
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


    def __init__(self, id, width, height, pos_x=-1, pos_y=-1, color=(0, 0, 0), **kwargs):
        self.id = id
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
