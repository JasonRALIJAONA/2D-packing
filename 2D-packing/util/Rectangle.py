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

    