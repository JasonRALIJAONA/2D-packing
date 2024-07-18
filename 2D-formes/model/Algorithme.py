import copy
from util.Socle import Socle
from itertools import permutations , product
from util.Rectangle import Rectangle
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.affinity import rotate, translate

class Algorithme:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fits(forme, polygon_place, socle):
        # Check if the forme is within the socle boundaries
        if not forme.within(Polygon([(socle.pos_x, socle.pos_y), (socle.pos_x + socle.width, socle.pos_y), (socle.pos_x + socle.width, socle.pos_y + socle.height), (socle.pos_x, socle.pos_y + socle.height)])):
            return False

        # Check if the forme intersects with any of the placed polygons
        for placed in polygon_place:
            if forme.intersects(placed.perimetre):
                # If forme only touches the placed polygon (shares a boundary without overlapping), it's not considered an intersection
                if forme.touches(placed.perimetre):
                    continue
                return False

        return True
    
    # @staticmethod
    # def fits(forme, placed_polygons, socle):
    #     socle_polygon = Polygon([(socle.pos_x, socle.pos_y), 
    #                              (socle.pos_x + socle.width, socle.pos_y), 
    #                              (socle.pos_x + socle.width, socle.pos_y + socle.height), 
    #                              (socle.pos_x, socle.pos_y + socle.height)])
    #     if not forme.within(socle_polygon):
    #         return False
        
    #     for pp in placed_polygons:
    #         if forme.intersects(pp.perimetre):
    #             return False
            
    #     return True
    
    def heuristic(self, formes, socle):
        formes.sort(key=lambda f: max(f.width, f.height), reverse=True)
        placed_polygons = []

        for form in formes:
            placed = False
            for rotation in [0, 90, 180, 270]:
                rotated_perimetre = rotate(form.cree_perimetre(0), rotation, origin='centroid')
                for x in range(socle.width):
                    for y in range(socle.height):
                        translated_perimetre = translate(rotated_perimetre, xoff=x, yoff=y)
                        form.pos_x, form.pos_y = x, y
                        form.perimetre = translated_perimetre
                        if self.fits(form.perimetre, placed_polygons, socle):
                            placed_polygons.append(form)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break
        
        for placed in placed_polygons:
            for form in formes:
                if placed.id == form.id:
                    form.pos_x = placed.pos_x
                    form.pos_y = placed.pos_y
                    form.perimetre = placed.perimetre
                    break

    def brut_force(self, formes, socle):
        for perm in permutations(formes):
            placed_polygons = []
            success = True
            perm_copy = [copy.deepcopy(rect) for rect in perm]
            for rect in perm_copy:
                for x in range(socle.width - rect.width + 1):
                    for y in range(socle.height - rect.height + 1):
                        rect.pos_x, rect.pos_y = x, y
                        rect.perimetre = rect.cree_perimetre(0)
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
    
    def brut_force_rotate(self, formes, socle):
        finished = False
        for perm in permutations(formes):
            if finished:
                break
            # Each element in orientations is a tuple of integers (0, 90, 180) representing the rotation angle for each shape
            for orientations in product([0,90,180], repeat=len(formes)):
                if finished:
                    break
                placed_forms = []
                success = True
                for form, rotation_angle in zip(perm, orientations):
                    # Rotate the rectangle based on the specified angle
                    form = form.rotate(rotation_angle)
                    
                    # Try placing the rectangle in the first position where it fits
                    for x in range(socle.width - form.width + 1):
                        for y in range(socle.height - form.height + 1):
                            form.pos_x, form.pos_y = x, y
                            form.perimetre = form.cree_perimetre(rotation_angle)
                            if Algorithme.fits(form.perimetre, placed_forms, socle):
                                form_copy = form.copy()
                                placed_forms.append(form_copy)  # Assume there's a method to copy the shape
                                break
                        else:
                            continue
                        break
                    else:
                        success = False
                        break

                if success:
                    # Successfully placed all rectangles, can finish
                    finished = True
                    break

        for placed in placed_forms:
            for form in formes:
                if placed.id == form.id:
                    form.pos_x = placed.pos_x
                    form.pos_y = placed.pos_y
                    form.perimetre = placed.perimetre
                    break