from util.Objet import Objet
from model.Algorithme import Algorithme
from itertools import permutations

# cree 10 objet de taille 1
objets=[]
objets.append(Objet(0,10))
objets.append(Objet(1,20))
objets.append(Objet(2,15))
objets.append(Objet(3,25))
objets.append(Objet(4,30))

taille_bac=50

# for p in perm:
#     print(f"[{', '.join([str(o.id) for o in p])}]")


bacs=Algorithme.brut_force(objets,taille_bac)

# for bac in bacs:
#     print("Bac ",bac.id," : ",[objet.id for objet in bac.objets])

for objet in objets:
    print("Objet ",objet.id," de taille: ",objet.taille,"dans le bac ",objet.id_bac)