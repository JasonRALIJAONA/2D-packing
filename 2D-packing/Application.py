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
        self.master.geometry("400x700")
        self.pack(padx=10, pady=10)
        self.create_widgets()
        self.rectangles = []
        self.socle = None

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

        # Bouton pour charger les données
        self.load_data_button = ttk.Button(self, text="Charger Données", command=self.load_data)
        self.load_data_button.pack(pady=10)

        self.label_height = ttk.Label(self, text="Choisir l'algorithme:")
        self.label_height.pack(pady=5)
        # Combobox pour choisir l'algorithme
        self.algorithm_combobox = ttk.Combobox(self, values=["Next_fit", "First_fit", "Best_fit"])
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.pack(pady=5)

        # Bouton pour exécuter l'algorithme sélectionné
        self.execute_button = ttk.Button(self, text="Exécuter l'Algorithmme", command=lambda: self.run_algorithm(self.algorithm_combobox.get()))
        self.execute_button.pack(pady=10)

        # Bouton pour sauvegarder les données
        self.save_data_button = ttk.Button(self, text="Sauvegarder Données", command=self.save_data)
        self.save_data_button.pack(pady=10)

        self.result_text = tk.Text(self, wrap=tk.WORD, height=10)
        self.result_text.pack(pady=10)

    def save_data(self):
        data = {
            "rectangles": [rect.__dict__ for rect in self.rectangles],
            "socle": self.socle.__dict__ if self.socle else None,
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.result_text.insert(tk.END, "Données sauvegardées avec succès.\n")
            
    def load_data(self):
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
                    socle_data['height'],
                    socle_data.get('pos_x_actuel', 0),
                    socle_data.get('pos_y_actuel', 0),
                    socle_data.get('rectangles', []),
                    socle_data.get('etages', [])
                )
                # Mettre à jour les champs d'entrée avec les valeurs du socle
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
        try:
            try:
                self.socle_width = int(self.entry_socle_width.get())
                self.socle_height = int(self.entry_socle_height.get())
                self.socle = Socle(0, 0, self.socle_width, self.socle_height)
            except ValueError:
                self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur du socle.\n")
                return
            
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            rectangle = Rectangle(len(self.rectangles) + 1, width, height)
            self.rectangles.append(rectangle)
            self.update_result_text()
        except ValueError:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des nombres valides pour la largeur et la hauteur des rectangles.\n")

    def update_result_text(self):
        self.result_text.delete('1.0', tk.END)
        for rect in self.rectangles:
            self.result_text.insert(tk.END, f"Rectangle {rect.id}: ({rect.pos_x}, {rect.pos_y})\n")

    def run_algorithm(self, algorithm_name):
        

        algo = Algorithme()
        if algorithm_name == "Next_fit":
            algo.next_fit_dh(self.rectangles, self.socle)
        elif algorithm_name == "First_fit":
            algo.first_fit_dh(self.rectangles, self.socle)
        elif algorithm_name == "Best_fit":
            algo.best_fit_dh(self.rectangles, self.socle)
        else:
            self.result_text.insert(tk.END, "Algorithme non trouvé.\n")
            return

        self.update_result_text()
        self.draw_canvas(algorithm_name)

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

        for index, rect in enumerate(self.rectangles):
            if rect.pos_x != -1:
                rect_color_hex = "#" + "".join([f"{x:02X}" for x in rect.color])
                canvas.create_rectangle(rect.pos_x, rect.pos_y, rect.pos_x + rect.width, rect.pos_y + rect.height, fill=rect_color_hex, outline=rect_color_hex)
                canvas.create_text(rect.pos_x + rect.width / 2, rect.pos_y + rect.height / 2, text=str(index + 1), font=("Arial", 5))

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
