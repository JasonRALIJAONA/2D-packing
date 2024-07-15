import copy
from util.Socle import Socle
from itertools import permutations , product
from util.Rectangle import Rectangle
from shapely.geometry import Polygon
from shapely.ops import unary_union

class Algorithme:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fits(forme, polygon_place, socle):
        # Check if the forme is within the socle boundaries
        if not forme.within(Polygon([(socle.pos_x, socle.pos_y), (socle.pos_x + socle.width, socle.pos_y), (socle.pos_x + socle.width, socle.pos_y + socle.height), (socle.pos_x, socle.pos_y + socle.height)])):
            return False

        # Combine all placed polygons into a single union polygon for efficient overlap checking
        if polygon_place:
            placed_union = unary_union([pp.perimetre for pp in polygon_place])
            # Check if the forme intersects with the placed_union
            if forme.intersects(placed_union):
                # If forme only touches the placed_union (shares a boundary without overlapping), it's not considered an intersection
                if forme.touches(placed_union):
                    return True
                return False
        # If there are no placed polygons, no need to check for intersection
        return True
    
    def brut_force(self, formes, socle):
        for perm in permutations(formes):
            placed_polygons = []
            success = True
            perm_copy = [copy.deepcopy(rect) for rect in perm]
            for rect in perm_copy:
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
        
        