class Algorithme:
    def __init__(self) -> None:
        pass

    def sort_by_height(self, rectangles):
        return sorted(rectangles, key=lambda x: x.height, reverse=True)
    
    def next_fit_dh (self ,rectangles , socle):
        rect=self.sort_by_height(rectangles)

        for i in range (len(rect)):
            if rect[i].height <= socle.height and rect[i].width <= socle.width:
                width_restant , height_restant = socle.espace_restant()

                if rect[i].width <= width_restant:
                    socle.add_rect(rect[i])

    

                
                