from util.Rectangle import Rectangle
from util.Socle import Socle
from model.Algorithme import Algorithme


rectangles=[]
rectangles.append(Rectangle(1,20,50))
rectangles.append(Rectangle(2,30,40))
rectangles.append(Rectangle(3,20,35))
rectangles.append(Rectangle(4,20,30))
rectangles.append(Rectangle(5,20,20))
rectangles.append(Rectangle(6,20,10))

socle = Socle(0,0,50,100) 

algo=Algorithme()
algo.next_fit_dh(rectangles,socle)

for rect in rectangles:
    print(f"({rect.id}) x: {rect.pos_x}  ,  y: {rect.pos_y} , width: {rect.width} , height: {rect.height}")