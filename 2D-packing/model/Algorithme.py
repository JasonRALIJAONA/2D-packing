from util.Socle import Socle

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
                if (i==0):
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
                if (i==0):
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

    

                
                