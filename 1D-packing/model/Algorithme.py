from util.Bac import Bac

class Algorithme:
    def __init__(self) -> None:
        pass

    def first_fit (objets , taille_bac):
        bacs=[]

        # ajout du premier bac
        id_bac=0
        bacs.append(Bac(id_bac,taille_bac))
        id_bac+=1

        for objet in objets:
            for bac in bacs:
                if bac.taille_restante() - objet.taille >= 0:
                    bac.objets.append(objet)
                    objet.id_bac=bac.id
                    break
                elif (bac.id == len(bacs)-1):
                    nouveau_bac=Bac(id_bac,taille_bac)
                    nouveau_bac.objets.append(objet)
                    bacs.append(nouveau_bac)
                    objet.id_bac=nouveau_bac.id
                    id_bac+=1
                    break
                    

        return bacs


        