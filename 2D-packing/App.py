from util.Rectangle import Rectangle
from util.Socle import Socle
from model.Algorithme import Algorithme


rectangles=[]
rectangles.append(Rectangle(1,30,50))
rectangles.append(Rectangle(2,20,40))
rectangles.append(Rectangle(3,55,30))
rectangles.append(Rectangle(4,20,30))
rectangles.append(Rectangle(5,40,20))
rectangles.append(Rectangle(6,10,10))

socle = Socle(0,0,100,100) 

algo=Algorithme()
# algo.best_fit_dh(rectangles,socle)
algo.brut_force(rectangles,socle)


for rect in rectangles:
    print(f"({rect.id}) x: {rect.pos_x}  ,  y: {rect.pos_y} , width: {rect.width} , height: {rect.height}")