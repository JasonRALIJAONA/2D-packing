class Algorithme:
    def __init__(self) -> None:
        pass

    def sort_by_height(self, rectangles):
        return sorted(rectangles, key=lambda x: x.height, reverse=True)
    
    