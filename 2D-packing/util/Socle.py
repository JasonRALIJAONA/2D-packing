class Socle:
    def __init__(self,pos_x, pos_y, width, height):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_x_actuel = pos_x
        self.pos_y_actuel = pos_y
        self.rectangles= []
        self.etages = []

    def __init__(self, pos_x, pos_y, width, height, **kwargs):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.pos_x_actuel = pos_x
        self.pos_y_actuel = pos_y
        self.rectangles= []
        self.etages = []

    def add_rect(self, rect):
        self.rectangles.append(rect)
        rect.pos_x = self.pos_x_actuel
        rect.pos_y = self.pos_y_actuel
        self.pos_x_actuel += rect.width

    def espace_restant(self):
        width_restant = self.width - sum([r.width for r in self.rectangles])
        height_restant = self.height - sum([r.height for r in self.rectangles])

        return width_restant, height_restant

    def hauteur_etage_restant(self):
        return self.height - sum([r.height for r in self.etages])
    