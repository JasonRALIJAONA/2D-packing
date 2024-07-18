import math
import random
from shapely.geometry import Polygon
from shapely.affinity import rotate

class Triangle:
    def __init__(self,id ,base, **kwargs):
        self.id = id
        self.width = base
        self.height = (int)(math.sqrt(3)/2)*base
        self.pos_x = -1
        self.pos_y = -1
        self.perimetre = self.cree_perimetre(0)
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def cree_perimetre(self , angle):
        # Height of the equilateral triangle
        h = (int)((math.sqrt(3) / 2) * self.width)
        # Distance from the center to a vertex along the y-axis
        dy = (int)(h / 2)

        # Calculate vertices based on the center (center_x, center_y)
        A = (self.pos_x - self.width / 2, self.pos_y - dy)
        B = (self.pos_x + self.width / 2, self.pos_y - dy)
        C = (self.pos_x, self.pos_y + (h - dy))

        p=Polygon([A, B, C])
        return rotate(p,angle,origin='center',use_radians=False)

    def copy(self):
        t= Triangle(self.id, self.width)
        t.pos_x = self.pos_x
        t.pos_y = self.pos_y
        t.perimetre = self.perimetre
        return t
    
    def rotate(self, angle):
        copie=self.copy()
        copie.perimetre = rotate(copie.perimetre,angle,origin='center',use_radians=False)
        return copie


    # def __init__(self, id, base, pos_x=-1, pos_y=-1, color=(0, 0, 0), **kwargs):
    #     self.id = id
    #     self.width = base
    #     self.pos_x = pos_x
    #     self.pos_y = pos_y
    #     self.perimetre = self.cree_perimetre()
    #     self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))