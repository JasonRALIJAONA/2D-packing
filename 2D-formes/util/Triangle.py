import math
import random
from shapely.geometry import Polygon

class Triangle:
    def __init__(self,id ,base, **kwargs):
        self.id = id
        self.width = base
        self.height = (int)(math.sqrt(3)/2)*base
        self.pos_x = -1
        self.pos_y = -1
        self.perimetre = self.cree_perimetre()
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def cree_perimetre(self):
        A=(self.pos_x,self.pos_y)
        B=(self.pos_x+self.width,self.pos_y)
        C=(self.pos_x+(self.width/2),self.pos_y+((math.sqrt(3)/2)*self.width))

        return Polygon([A,B,C])

    def copy(self):
        return Triangle(self.id, self.width)

    # def __init__(self, id, base, pos_x=-1, pos_y=-1, color=(0, 0, 0), **kwargs):
    #     self.id = id
    #     self.width = base
    #     self.pos_x = pos_x
    #     self.pos_y = pos_y
    #     self.perimetre = self.cree_perimetre()
    #     self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))