from util.Socle import Socle
from itertools import permutations , product
from util.Rectangle import Rectangle

class Algorithme:
    def __init__(self) -> None:
        pass

    def sort_by_height(self, rectangles):
        return sorted(rectangles, key=lambda x: x.height, reverse=True)
    
    def next_fit_dh (self ,rectangles , socle):
        rect=self.sort_by_height(rectangles)
        ind_etage=0
        futur_etage_y=0
        for i in range (len(rect)):
            if rect[i].height <= socle.height and rect[i].width <= socle.width:
                if (len(socle.etages)==0):
                    futur_etage_y=rect[i].height
                    socle.etages.append(Socle(socle.pos_x,socle.pos_y_actuel,socle.width,rect[i].height))

                etage=socle.etages[ind_etage]
                width_restant, height_restant = etage.espace_restant()

                if (rect[i].width <= width_restant):
                    etage.add_rect(rect[i])
                elif (rect[i].height <= socle.hauteur_etage_restant()):
                    socle.pos_y_actuel += futur_etage_y
                    futur_etage_y = rect[i].height
                    ind_etage+=1
                    socle.etages.append(Socle(socle.pos_x , socle.pos_y_actuel, socle.width , rect[i].height))
                    temp=socle.etages[ind_etage]
                    temp.add_rect(rect[i])

                

    def first_fit_dh(self, rectangles, socle):
        rect = self.sort_by_height(rectangles)
        futur_etage_y = 0

        for i in range(len(rect)):
            if rect[i].height <= socle.height and rect[i].width <= socle.width:
                if (len(socle.etages)==0):
                    futur_etage_y=rect[i].height
                    socle.etages.append(Socle(socle.pos_x,socle.pos_y_actuel,socle.width,rect[i].height))

                for j in range(len(socle.etages)):
                    etage=socle.etages[j]
                    width_restant, height_restant = etage.espace_restant()

                    if (rect[i].width <= width_restant):
                        etage.add_rect(rect[i])
                        break
                    elif (rect[i].height <= socle.hauteur_etage_restant() and j==len(socle.etages)-1):
                        socle.pos_y_actuel += futur_etage_y
                        futur_etage_y = rect[i].height
                        socle.etages.append(Socle(socle.pos_x , socle.pos_y_actuel, socle.width , rect[i].height))
                        temp=socle.etages[-1]
                        temp.add_rect(rect[i])
                        break

    def best_fit_dh(self, rectangles, socle):
        rect = self.sort_by_height(rectangles)
        futur_etage_y = 0

        for i in range(len(rect)):
            if rect[i].height <= socle.height and rect[i].width <= socle.width:
                if (len(socle.etages)==0):
                    futur_etage_y=rect[i].height
                    socle.etages.append(Socle(socle.pos_x,socle.pos_y_actuel,socle.width,rect[i].height)) 

                # id de l'etage et le width restant
                etage_choisi=(0,float("inf"))

                for j in range(len(socle.etages)):
                    etage=socle.etages[j]
                    width_restant, height_restant = etage.espace_restant()

                    if (rect[i].width <= width_restant and (width_restant-rect[i].width)<etage_choisi[1]):
                        etage_choisi=(j,width_restant-rect[i].width)
                
                    elif (rect[i].height <= socle.hauteur_etage_restant() and j==len(socle.etages)-1) and etage_choisi[1]==float("inf"):
                        socle.pos_y_actuel += futur_etage_y
                        futur_etage_y = rect[i].height
                        socle.etages.append(Socle(socle.pos_x , socle.pos_y_actuel, socle.width , rect[i].height))
                        temp=socle.etages[-1]
                        temp.add_rect(rect[i])
                        break

                if etage_choisi[1]!=float("inf"):
                    socle.etages[etage_choisi[0]].add_rect(rect[i])

    @staticmethod
    def fits(rect, placed_rects, socle):
        for pr in placed_rects:
            if not (rect.pos_x + rect.width <= pr.pos_x or rect.pos_x >= pr.pos_x + pr.width or
                    rect.pos_y + rect.height <= pr.pos_y or rect.pos_y >= pr.pos_y + pr.height):
                return False  # Overlaps with an already placed rectangle
        return rect.pos_x + rect.width <= socle.width and rect.pos_y + rect.height <= socle.height
    

    
    def brut_force(self, rectangles, socle):
        # Try each permutation of rectangles
        for perm in permutations(rectangles):
            placed_rects = []
            success = True
            for rect in perm:
                # Try placing the rectangle in the first position where it fits
                for x in range(socle.width - rect.width + 1):
                    for y in range(socle.height - rect.height + 1):
                        rect.pos_x, rect.pos_y = x, y
                        if Algorithme.fits(rect, placed_rects, socle):
                            placed_rects.append(rect)
                            break
                    else:
                        continue
                    break
                else:
                    success = False
                    break
    
            if success:
                break

        #update the posx and posy of each rectangle 
        for rec in placed_rects:
            for org_rec in rectangles:
                if rec.id == org_rec.id:
                    org_rec.pos_x = rec.pos_x
                    org_rec.pos_y = rec.pos_y
                    break

    def brut_force_rotate(self ,rectangles, socle):
        finished=False
        for perm in permutations(rectangles):
            if finished:
                break
            # Each element in orientations is a tuple of booleans representing whether to rotate each rectangle
            for orientations in product([False, True], repeat=len(rectangles)):
                if finished:
                    break
                placed_rects = []
                success = True
                for rect, rotate in zip(perm, orientations):
                    original_width, original_height = rect.width, rect.height
                    # Rotate the rectangle if specified
                    if rotate:
                        rect.rotate()
                    
                    # Try placing the rectangle in the first position where it fits
                    for x in range(socle.width - rect.width + 1):
                        for y in range(socle.height - rect.height + 1):
                            rect.pos_x, rect.pos_y = x, y
                            if Algorithme.fits(rect, placed_rects, socle):
                                rect_copy = Rectangle(rect.id, rect.width, rect.height, x, y, rect.color)
                                placed_rects.append(rect_copy)  # Assume there's a method to copy the rectangle
                                break
                        else:
                            continue
                        break
                    else:
                        success = False
                        # Reset the rectangle to its original orientation if it was rotated
                        rect.rotate()
                        break
                    
                    # Reset the rectangle to its original orientation for the next iteration
                    if rotate:
                        rect.rotate()

                if success:
                    finished = True
                    break
                
        for rec in placed_rects:
            for org_rec in rectangles:
                if rec.id == org_rec.id:
                    org_rec.pos_x = rec.pos_x
                    org_rec.pos_y = rec.pos_y
                    break

        
                   
                