import tkinter as tk
from tkinter import ttk
from util.Rectangle import Rectangle
from util.Socle import Socle
from model.Algorithme import Algorithme

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Formulaire")
        self.master.geometry("300x500")  # Fixed window size
        self.pack(padx=10, pady=10)
        self.create_widgets()
        self.rectangles = []
        self.socle = None  # Initialisation temporaire

    def create_widgets(self):
        # Nouvelles entrées pour la taille du socle
        self.label_socle_width = ttk.Label(self, text="Largeur du socle:")
        self.label_socle_width.pack(pady=5)
        self.entry_socle_width = ttk.Entry(self)
        self.entry_socle_width.pack(pady=5)

        self.label_socle_height = ttk.Label(self, text="Hauteur du socle:")
        self.label_socle_height.pack(pady=5)
        self.entry_socle_height = ttk.Entry(self)
        self.entry_socle_height.pack(pady=5)

        # Widgets pour saisir les dimensions des rectangles
        self.label_width = ttk.Label(self, text="Largeur:")
        self.label_width.pack(pady=5)
        self.entry_width = ttk.Entry(self)
        self.entry_width.pack(pady=5)

        self.label_height = ttk.Label(self, text="Hauteur:")
        self.label_height.pack(pady=5)
        self.entry_height = ttk.Entry(self)
        self.entry_height.pack(pady=5)

        # Bouton pour ajouter un rectangle
        self.add_button = ttk.Button(self, text="Ajouter Rectangle", command=self.add_rectangle)
        self.add_button.pack(pady=10)

        # Bouton pour exécuter l'algorithme de placement
        self.run_button = ttk.Button(self, text="Exécuter Placement", command=self.run_algorithm)
        self.run_button.pack(pady=10)

        self.result_text = tk.Text(self, wrap=tk.WORD, height=10)
        self.result_text.pack(pady=10)

    def add_rectangle(self):
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            rectangle = Rectangle(len(self.rectangles)+1, width, height)
            self.rectangles.append(rectangle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur des rectangles.\n")

    def update_result_text(self):
        self.result_text.delete('1.0', tk.END)
        for rect in self.rectangles:
            self.result_text.insert(tk.END, f"Rectangle {rect.id}: ({rect.pos_x}, {rect.pos_y})\n")

    def run_algorithm(self):
        try:
            self.socle_width = int(self.entry_socle_width.get())
            self.socle_height = int(self.entry_socle_height.get())
            self.socle = Socle(0, 0, self.socle_width, self.socle_height)
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")
            return

        algo = Algorithme()
        algo.next_fit_dh(self.rectangles, self.socle)
        self.update_result_text()
        self.draw_canvas()

    def draw_canvas(self):
        try:
            socle_width = int(self.entry_socle_width.get())
            socle_height = int(self.entry_socle_height.get())
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")
            return

        canvas_window = tk.Toplevel(self.master)
        canvas_window.title("2D Packing")
        canvas_window.geometry(f"{socle_width}x{socle_height}")
        canvas = tk.Canvas(canvas_window, bg='white', width=socle_width, height=socle_height)
        canvas.pack(fill=tk.BOTH, expand=True)

        socle_color = 'lightblue'
        canvas.create_rectangle(0, 0, socle_width, socle_height, fill=socle_color, outline=socle_color)

        for index, rect in enumerate(self.rectangles):
            if rect.pos_x != -1:
                rect_color_hex = "#" + "".join([f"{x:02X}" for x in rect.color])
                canvas.create_rectangle(rect.pos_x, rect.pos_y, rect.pos_x + rect.width, rect.pos_y + rect.height, fill=rect_color_hex, outline=rect_color_hex)
                canvas.create_text(rect.pos_x + rect.width / 2, rect.pos_y + rect.height / 2, text=str(index+1), font=("Arial", 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
