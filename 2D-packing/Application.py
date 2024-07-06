import tkinter as tk
import json
from tkinter import ttk
from util.Rectangle import Rectangle
from util.Socle import Socle
from model.Algorithme import Algorithme

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Formulaire")
        self.master.geometry("600x800")
        self.pack(padx=10, pady=10)
        
        self.rectangles = []
        self.socle = None

        self.create_socle_form()
        self.create_rectangle_form()
        self.create_algorithm_execution_form()
        self.create_result_text()

    def create_socle_form(self):
        # Formulaire pour le socle, chargement et sauvegarde
        socle_frame = ttk.LabelFrame(self, text="Socle - Chargement - Sauvegarde")
        socle_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_socle_width = ttk.Label(socle_frame, text="Largeur du socle:")
        self.label_socle_width.pack(pady=5)
        self.entry_socle_width = ttk.Entry(socle_frame)
        self.entry_socle_width.pack(pady=5)

        self.label_socle_height = ttk.Label(socle_frame, text="Hauteur du socle:")
        self.label_socle_height.pack(pady=5)
        self.entry_socle_height = ttk.Entry(socle_frame)
        self.entry_socle_height.pack(pady=5)

        self.validate_socle_button = ttk.Button(socle_frame, text="Valider Socle", command=self.validate_socle)
        self.validate_socle_button.pack(pady=10)

        self.load_data_button = ttk.Button(socle_frame, text="Charger Données", command=self.load_data)
        self.load_data_button.pack(pady=10)

        self.save_data_button = ttk.Button(socle_frame, text="Sauvegarder Données", command=self.save_data)
        self.save_data_button.pack(pady=10)

    def create_rectangle_form(self):
        # Formulaire pour ajouter des rectangles
        rectangle_frame = ttk.LabelFrame(self, text="Rectangles")
        rectangle_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_width = ttk.Label(rectangle_frame, text="Largeur:")
        self.label_width.pack(pady=5)
        self.entry_width = ttk.Entry(rectangle_frame)
        self.entry_width.pack(pady=5)

        self.label_height = ttk.Label(rectangle_frame, text="Hauteur:")
        self.label_height.pack(pady=5)
        self.entry_height = ttk.Entry(rectangle_frame)
        self.entry_height.pack(pady=5)

        self.add_button = ttk.Button(rectangle_frame, text="Ajouter Rectangle", command=self.add_rectangle)
        self.add_button.pack(pady=10)

    def create_algorithm_execution_form(self):
        # Formulaire pour l'exécution de l'algorithme
        algorithm_frame = ttk.LabelFrame(self, text="Algo")
        algorithm_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.label_algorithm = ttk.Label(algorithm_frame, text="Choisir l'algorithme:")
        self.label_algorithm.pack(pady=5)
        self.algorithm_combobox = ttk.Combobox(algorithm_frame, values=["Next_fit", "First_fit", "Best_fit", "Brut_force"])
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.pack(pady=5)

        self.execute_button = ttk.Button(algorithm_frame, text="Exécuter l'Algorithmme", command=self.execute_algorithm)
        self.execute_button.pack(pady=10)

    def create_result_text(self):
        # Zone de texte pour afficher les résultats
        result_frame = ttk.LabelFrame(self, text="Résultats")
        result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def save_data(self):
        # Sauvegarde des données dans un fichier JSON
        data = {
            "rectangles": [rect.__dict__ for rect in self.rectangles],
            "socle": self.socle.__dict__ if self.socle else None,
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.result_text.insert(tk.END, "Données sauvegardées avec succès.\n")

    def load_data(self):
        # Chargement des données depuis un fichier JSON
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                self.rectangles = [
                    Rectangle(item['id'], item['width'], item['height'], item.get('pos_x', -1), item.get('pos_y', -1), item.get('color', (0, 0, 0)))
                    for item in data['rectangles']
                ]
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
        except FileNotFoundError:
            self.result_text.insert(tk.END, "Le fichier de données n'a pas été trouvé.\n")
        except KeyError as e:
            self.result_text.insert(tk.END, f"Erreur lors du chargement des données: clé manquante {e}\n")

    def add_rectangle(self):
        # Ajout d'un rectangle à la liste
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            rectangle = Rectangle(len(self.rectangles) + 1, width, height)
            self.rectangles.append(rectangle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur des rectangles.\n")

    def validate_socle(self):
        try:
            width = int(self.entry_socle_width.get())
            height = int(self.entry_socle_height.get())
            self.socle = Socle(0, 0, width, height)
            # self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")

    def update_result_text(self):
        # Mise à jour du texte de résultat
        self.result_text.delete('1.0', tk.END)
        for rect in self.rectangles:
            self.result_text.insert(tk.END, f"({rect.id}) x: {rect.pos_x}  ,  y: {rect.pos_y} , width: {rect.width} , height: {rect.height}\n")

    def execute_algorithm(self):
        # Exécution de l'algorithme sélectionné
        algorithm_name = self.algorithm_combobox.get()
        algo = Algorithme()
        if algorithm_name == "Next_fit":
            algo.next_fit_dh(self.rectangles, self.socle)
        elif algorithm_name == "First_fit":
            algo.first_fit_dh(self.rectangles, self.socle)
        elif algorithm_name == "Best_fit":
            algo.best_fit_dh(self.rectangles, self.socle)
        elif algorithm_name == "Brut_force":
            algo.brut_force(self.rectangles, self.socle)
        else:
            self.result_text.insert(tk.END, "Algorithme non trouvé.\n")
            return
        self.update_result_text()
        self.draw_canvas(algorithm_name)

    def draw_canvas(self, title):
        # Dessin du canvas avec les rectangles placés
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

        for index, rect in enumerate(self.rectangles):
            if rect.pos_x != -1:
                rect_color_hex = "#" + "".join([f"{x:02X}" for x in rect.color])
                canvas.create_rectangle(rect.pos_x, rect.pos_y, rect.pos_x + rect.width, rect.pos_y + rect.height, fill=rect_color_hex, outline=rect_color_hex)
                canvas.create_text(rect.pos_x + rect.width / 2, rect.pos_y + rect.height / 2, text=str(index + 1), font=("Arial", 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
