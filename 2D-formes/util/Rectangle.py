import random
from shapely.geometry import box

class Rectangle:
    def __init__(self,id ,width, height):
        self.id = id
        self.width = width
        self.height = height
        self.pos_x = -1
        self.pos_y = -1
        self.perimetre = self.cree_perimetre(0)
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def cree_perimetre(self , angle):
        return box(self.pos_x, self.pos_y, self.pos_x + self.width, self.pos_y + self.height)
    
    def copy(self):
        rec = Rectangle(self.id, self.width, self.height)
        rec.pos_x = self.pos_x
        rec.pos_y = self.pos_y
        rec.perimetre = self.perimetre
        return rec

    def __init__(self, id, width, height, pos_x=-1, pos_y=-1, color=(0, 0, 0), **kwargs):
        self.id = id
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.perimetre = self.cree_perimetre(0)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def rotate(self, angle):
        copie = self.copy()
        if angle == 90:
            copie.width , copie.height = self.height , self.width
            copie.perimetre = copie.cree_perimetre(0)
        
        return copie
    