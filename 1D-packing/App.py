from util.Objet import Objet
from model.Algorithme import Algorithme

# cree 10 objet de taille 1
objets=[]
objets.append(Objet(0,1))
objets.append(Objet(1,2))
objets.append(Objet(2,5))
objets.append(Objet(3,1))
objets.append(Objet(4,1))
objets.append(Objet(5,1))
objets.append(Objet(6,1))
objets.append(Objet(7,1))
objets.append(Objet(8,1))
objets.append(Objet(9,1))

taille_bac=5

bacs=Algorithme.best_fit(objets,taille_bac)


# for bac in bacs:
#     print("Bac ",bac.id," : ",[objet.id for objet in bac.objets])

for objet in objets:
    print("Objet ",objet.id," de taille: ",objet.taille,"dans le bac ",objet.id_bac)