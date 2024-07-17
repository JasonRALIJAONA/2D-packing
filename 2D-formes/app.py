from shapely import Point, Polygon
from util.Socle import Socle
from util.Cercle import Cercle
from util.Rectangle import Rectangle
from model.Algorithme import Algorithme
from util.Triangle import Triangle

formes = []
socle = Socle(0,0,100,100)

formes.append(Rectangle(1,30,50))
formes.append(Rectangle(2,20,40))
formes.append(Rectangle(3,55,30))
formes.append(Rectangle(4,20,30))
formes.append(Rectangle(5,40,20))
formes.append(Rectangle(6,10,10))

algo = Algorithme()
algo.brut_force_rotate(formes,socle)

for forme in formes:
    print(f"({forme.id}) : x : {forme.pos_x} , y : {forme.pos_y} , rayon : {forme.width}")


