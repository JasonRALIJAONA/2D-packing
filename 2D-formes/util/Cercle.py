import random
from shapely.geometry import Point

# cx : centre x
class Cercle:
    def __init__(self,id,rayon, **kwargs):
        self.id = id
        self.pos_x = -1
        self.pos_y = -1
        self.rayon = rayon
        self.width = rayon
        self.height = rayon
        self.perimetre = self.cree_perimetre()
        # a random color
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


    def cree_perimetre(self):
        centre=Point(self.pos_x,self.pos_y)
        return centre.buffer(self.rayon)
    
    def copy(self):
        return Cercle(self.id,self.rayon)

    # def __init__(self, id, pos_x=-1, pos_y=-1, rayon=10,  color=(0, 0, 0), **kwargs):
    #     self.id = id
    #     self.centre = Point(pos_x, pos_y)
    #     self.rayon = rayon
    #     self.width = rayon
    #     self.height = rayon
    #     self.pos_x=pos_x
    #     self.pos_y=pos_y
    #     self.perimetre = self.cree_perimetre()
    #     self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))