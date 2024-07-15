import tkinter as tk
import json
from tkinter import ttk
from shapely.geometry import Polygon
from util.Rectangle import Rectangle
from util.Cercle import Cercle
from util.Triangle import Triangle
from util.Socle import Socle
from model.Algorithme import Algorithme

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Formulaire")
        self.master.geometry("300x600")
        self.pack(padx=10, pady=10)
        self.create_socle_widgets()
        self.create_shape_widgets()
        self.rectangles = []
        self.cercles = []
        self.triangles = []
        self.socle = None

    def create_socle_widgets(self):
        self.frame_socle = ttk.Frame(self)
        self.frame_socle.pack(pady=10, padx=10, fill=tk.BOTH)

        ttk.Label(self.frame_socle, text="Dimensions du Socle").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.frame_socle, text="Largeur du socle:").grid(row=1, column=0, sticky=tk.W)
        self.entry_socle_width = ttk.Entry(self.frame_socle)
        self.entry_socle_width.grid(row=1, column=1)

        ttk.Label(self.frame_socle, text="Hauteur du socle:").grid(row=2, column=0, sticky=tk.W)
        self.entry_socle_height = ttk.Entry(self.frame_socle)
        self.entry_socle_height.grid(row=2, column=1)

        ttk.Button(self.frame_socle, text="Valider Socle", command=self.validate_socle).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame_socle, text="Charger Données", command=self.load_data).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame_socle, text="Sauvegarder Données", command=self.save_data).grid(row=5, column=0, columnspan=2, pady=5)

    def validate_socle(self):
        try:
            self.socle_width = int(self.entry_socle_width.get())
            self.socle_height = int(self.entry_socle_height.get())
            self.socle = Socle(0, 0, self.socle_width, self.socle_height)
            self.result_text.insert(tk.END, f"Socle validé: {self.socle_width} x {self.socle_height}\n")
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")


    def create_shape_widgets(self):
        self.frame_shapes = ttk.Frame(self)
        self.frame_shapes.pack(pady=10, padx=10, fill=tk.BOTH)

        ttk.Label(self.frame_shapes, text="Ajouter des Formes").grid(row=0, column=0, columnspan=2, pady=10)

        # Rectangle
        ttk.Label(self.frame_shapes, text="Largeur:").grid(row=1, column=0, sticky=tk.W)
        self.entry_width = ttk.Entry(self.frame_shapes)
        self.entry_width.grid(row=1, column=1)

        ttk.Label(self.frame_shapes, text="Hauteur:").grid(row=2, column=0, sticky=tk.W)
        self.entry_height = ttk.Entry(self.frame_shapes)
        self.entry_height.grid(row=2, column=1)

        ttk.Button(self.frame_shapes, text="Ajouter Rectangle", command=self.add_rectangle).grid(row=3, column=0, columnspan=2, pady=5)

        # Cercle
        ttk.Label(self.frame_shapes, text="Rayon:").grid(row=4, column=0, sticky=tk.W)
        self.entry_radius = ttk.Entry(self.frame_shapes)
        self.entry_radius.grid(row=4, column=1)

        ttk.Button(self.frame_shapes, text="Ajouter Cercle", command=self.add_cercle).grid(row=5, column=0, columnspan=2, pady=5)

        # Triangle
        ttk.Label(self.frame_shapes, text="Base:").grid(row=6, column=0, sticky=tk.W)
        self.entry_base = ttk.Entry(self.frame_shapes)
        self.entry_base.grid(row=6, column=1)

        ttk.Button(self.frame_shapes, text="Ajouter Triangle", command=self.add_triangle).grid(row=7, column=0, columnspan=2, pady=5)

        ttk.Label(self.frame_shapes, text="Choisir l'algorithme:").grid(row=8, column=0, columnspan=2, pady=10)
        self.algorithm_combobox = ttk.Combobox(self.frame_shapes, values=["Brut_force"])
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.grid(row=9, column=0, columnspan=2)

        ttk.Button(self.frame_shapes, text="Exécuter l'Algorithme", command=lambda: self.run_algorithm(self.algorithm_combobox.get())).grid(row=10, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(self, wrap=tk.WORD, height=10)
        self.result_text.pack(pady=10)

    def polygon_to_serializable(self, polygon):
        return list(polygon.exterior.coords)

    def save_data(self):
        data = {
            "rectangles": [
                {key: value for key, value in rect.__dict__.items() if key != 'perimetre'} for rect in self.rectangles
            ],
            "cercles": [
                {key: value for key, value in cercle.__dict__.items() if key != 'perimetre'} for cercle in self.cercles
            ],
            "triangles": [
                {key: value for key, value in triangle.__dict__.items() if key != 'perimetre'} for triangle in self.triangles
            ],
            "socle": {key: value for key, value in self.socle.__dict__.items() if key != 'perimetre'} if self.socle else None,
        }
        with open('data2.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.result_text.insert(tk.END, "Données sauvegardées avec succès.\n")

    def serializable_to_polygon(self, coords):
        return Polygon(coords)  

    def load_data(self):
        with open('data2.json', 'r') as file:
            data = json.load(file)

        self.rectangles = [
            Rectangle(
                rect['id'],
                rect['width'],
                rect['height'],
                pos_x=rect['pos_x'],
                pos_y=rect['pos_y'],
                color=rect['color']
            ) for rect in data['rectangles']
        ]
        for rect in self.rectangles:
            rect.perimetre = rect.cree_perimetre()

        self.cercles = [
            Cercle(
                cercle['id'],
                rayon=cercle['rayon'],
                pos_x=cercle['pos_x'],
                pos_y=cercle['pos_y'],
                color=cercle['color']
            ) for cercle in data['cercles']
        ]
        for cercle in self.cercles:
            cercle.perimetre = cercle.cree_perimetre()

        self.triangles = [
            Triangle(
                triangle['id'],
                base=triangle['width'],
                pos_x=triangle['pos_x'],
                pos_y=triangle['pos_y'],
                color=triangle['color']
            ) for triangle in data['triangles']
        ]
        for triangle in self.triangles:
            triangle.perimetre = triangle.cree_perimetre()

        socle_data = data['socle']
        self.socle = Socle(
            socle_data['pos_x'],
            socle_data['pos_y'],
            socle_data['width'],
            socle_data['height']
        )
        self.entry_socle_width.delete(0, tk.END)
        self.entry_socle_width.insert(0, str(socle_data['width']))
        self.entry_socle_height.delete(0, tk.END)
        self.entry_socle_height.insert(0, str(socle_data['height']))
        self.update_result_text()

        self.result_text.insert(tk.END, "Données chargées avec succès.\n")



    def add_rectangle(self):
        if not self.socle:
            self.result_text.insert(tk.END, "Erreur: Veuillez valider le socle avant d'ajouter des formes.\n")
            return

        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            rectangle = Rectangle(len(self.rectangles) + 1, width, height)
            self.rectangles.append(rectangle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur des rectangles.\n")

    def add_cercle(self):
        try:
            rayon = int(self.entry_radius.get())
            cercle = Cercle(len(self.cercles) + 1, rayon)
            self.cercles.append(cercle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer un nombre valide pour le rayon du cercle.\n")

    def add_triangle(self):
        try:
            base = int(self.entry_base.get())
            triangle = Triangle(len(self.triangles) + 1, base)
            self.triangles.append(triangle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer un nombre valide pour la base du triangle.\n")

    def update_result_text(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Socle: {self.socle.width} x {self.socle.height}\n\n")
        for rect in self.rectangles:
            self.result_text.insert(tk.END, f"Rectangle ID: {rect.id}, Largeur: {rect.width}, Hauteur: {rect.height}, Position: ({rect.pos_x}, {rect.pos_y})\n")
        for cercle in self.cercles:
            self.result_text.insert(tk.END, f"Cercle ID: {cercle.id}, Rayon: {cercle.rayon}, Position: ({cercle.pos_x}, {cercle.pos_y})\n")
        for triangle in self.triangles:
            self.result_text.insert(tk.END, f"Triangle ID: {triangle.id}, Base: {triangle.width}, Position: ({triangle.pos_x}, {triangle.pos_y})\n")

    def run_algorithm(self, algorithm_name):
        if self.socle is None:
            self.result_text.insert(tk.END, "Erreur: Veuillez définir les dimensions du socle avant d'exécuter l'algorithme.\n")
            return

        formes = self.rectangles + self.cercles + self.triangles

        if algorithm_name == "Brut_force":
            Algorithme().brut_force(formes, self.socle)

        self.update_result_text()
        self.draw_canvas(f"Disposition avec {algorithm_name}")

    def draw_canvas(self, title):
        try:
            socle_width = int(self.entry_socle_width.get())
            socle_height = int(self.entry_socle_height.get())
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")
            return

        canvas_window = tk.Toplevel(self.master)
        canvas_window.title(title)
        canvas_window.geometry(f"{socle_width}x{socle_height}")
        canvas = tk.Canvas(canvas_window, bg='white', width=socle_width, height=socle_height)
        canvas.pack(fill=tk.BOTH, expand=True)

        socle_color = 'lightblue'
        canvas.create_rectangle(0, 0, socle_width, socle_height, fill=socle_color, outline=socle_color)

        def get_hex_color(color):
            return "#" + "".join([f"{x:02X}" for x in color])

        def draw_shape(shape, color):
            coords = list(shape.perimetre.exterior.coords)
            coords_flat = [coord for point in coords for coord in point]
            canvas.create_polygon(coords_flat, fill=color, outline=color)
            
            # Calculer le centre de la forme pour y placer l'ID
            center_x, center_y = shape.perimetre.centroid.x, shape.perimetre.centroid.y
            canvas.create_text(center_x, center_y, text=str(shape.id), fill='black')

        # Dessiner les rectangles
        for rect in self.rectangles:
            if rect.pos_x >= 0:
                draw_shape(rect, get_hex_color(rect.color))

        # Dessiner les cercles
        for cercle in self.cercles:
            if cercle.pos_x >= 0:
                draw_shape(cercle, get_hex_color(cercle.color))

        # Dessiner les triangles
        for triangle in self.triangles:
            if triangle.pos_x >= 0:
                draw_shape(triangle, get_hex_color(triangle.color))


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
