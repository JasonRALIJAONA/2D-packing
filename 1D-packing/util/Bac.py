class Bac:
    def __init__(self , id , taille):
        self.id=id
        self.taille=taille
        self.objets=[]

    def taille_restante(self):
        return self.taille - sum([objet.taille for objet in self.objets])
    
    

