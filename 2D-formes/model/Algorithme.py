from util.Socle import Socle
from itertools import permutations , product
from util.Rectangle import Rectangle
from shapely.geometry import Polygon

class Algorithme:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fits (forme , polygon_place , socle):
        if not forme.within(Polygon([(socle.pos_x, socle.pos_y), (socle.pos_x+socle.width, socle.pos_y), (socle.pos_x+socle.width , socle.pos_y+socle.height), (socle.pos_x, socle.pos_y+socle.height)])):
            return False
        
        for pp in polygon_place:
            if forme.intersects(pp.perimetre):
                return False
            
        return True
    
    def brut_force(self, formes, socle):
        for perm in permutations(formes):
            placed_polygons = []
            success = True
            for rect in perm:
                for x in range(socle.width - rect.width + 1):
                    for y in range(socle.height - rect.height + 1):
                        rect.pos_x, rect.pos_y = x, y
                        rect.perimetre = rect.cree_perimetre()
                        if Algorithme.fits(rect.perimetre, placed_polygons, socle):
                            placed_polygons.append(rect)
                            break
                    else:
                        continue
                    break
                else:
                    success = False
                    break

            if success:
                break
        
        for placed in placed_polygons:
            for form in formes:
                if placed.id == form.id:
                    form.pos_x = placed.pos_x
                    form.pos_y = placed.pos_y
                    form.perimetre = placed.perimetre
                    break

        
        