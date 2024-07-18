from shapely import Point, Polygon
from util.Socle import Socle
from util.Cercle import Cercle
from util.Rectangle import Rectangle
from model.Algorithme import Algorithme
from util.Triangle import Triangle

formes = []
socle = Socle(0,0,100,100)

formes.append(Cercle(1,25))
formes.append(Cercle(2,25))
formes.append(Cercle(3,25))
formes.append(Cercle(4,25))


algo = Algorithme()
algo.brut_force_rotate(formes,socle)

for forme in formes:
    print(f"({forme.id}) : x : {forme.pos_x} , y : {forme.pos_y} , rayon : {forme.width}")






