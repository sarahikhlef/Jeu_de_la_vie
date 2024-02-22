import tkinter as tk
from tkinter import Canvas
import numpy as np
import random
import threading
import time


# Classe Barriere pour synchroniser les threads
class Barriere:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait(self):
        with self.lock:
            self.count += 1
            if self.count == self.n:
                self.count = 0
                self.condition.notify_all()
            else:
                self.condition.wait()


# Classe pour gérer l'interface utilisateur
class GameOfLifeGUI:
    def __init__(self, master, matrix_size):
        self.master = master
        self.matrix_size = matrix_size
        self.barrier = Barriere(matrix_size * matrix_size + 1)  # +1 for the main thread
        self.M = init_matrix(matrix_size)
        self.new_M = np.copy(self.M)
        # Définir une taille maximale pour le canevas
        max_canvas_size = 800

        # Calculer la taille de chaque cellule pour que le canevas ne dépasse pas la taille maximale
        self.cell_size = max_canvas_size // matrix_size

        # Ajuster la taille du canevas en fonction du nombre de cellules et de leur taille
        canvas_size = self.cell_size * matrix_size

        self.canvas = Canvas(master, width=canvas_size, height=canvas_size)
        self.canvas.pack()
        self.threads = []
        self.running = True
        self.init_threads()
        self.draw_matrix()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.evolve()

    # Initialiser les threads pour chaque cellule de la matrice
    def init_threads(self):
        for i in range(1, self.matrix_size + 1):
            for j in range(1, self.matrix_size + 1):
                thread = threading.Thread(target=evolution, args=(i, j, self, self.barrier))
                thread.start()
                self.threads.append(thread)

    # Dessine la matrice sur le canevas
    def draw_matrix(self):
        self.canvas.delete("all")
        for i in range(1, self.matrix_size + 1):
            for j in range(1, self.matrix_size + 1):
                color = "black" if self.M[i][j] == 1 else "white"
                self.canvas.create_rectangle((j-1) * self.cell_size, (i-1) * self.cell_size,
                                             j * self.cell_size, i * self.cell_size, fill=color)

    def evolve(self):
        while self.running:
            # Attendre les threads
            self.barrier.wait()
            self.M = np.copy(self.new_M)
            self.draw_matrix()
            self.master.update()
            time.sleep(0.1)

    def on_closing(self):
        self.running = False
        self.master.destroy()


# Fonction pour initialiser la matrice avec des cellules aléatoires
def init_matrix(n):
    matrix = [[0] * (n + 2) for _ in range(n + 2)]
    for _ in range(random.randint(n, n * n)):
        i, j = random.randint(1, n), random.randint(1, n)
        matrix[i][j] = 1
    return matrix


# Fonction pour évoluer une cellule spécifique de la matrice
def evolution(i, j, gui, barrier):
    while gui.running:
        matrix = gui.M
        new_matrix = gui.new_M
        nb_neighbors = sum([matrix[i + dx][j + dy] for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not (dx == dy == 0)])
        new_matrix[i][j] = 1 if (matrix[i][j] == 1 and nb_neighbors in (2, 3)) or (matrix[i][j] == 0 and nb_neighbors == 3) else 0
        barrier.wait()
        time.sleep(0.3)


n = int(input("Saisir n: "))

root = tk.Tk()
game_of_life = GameOfLifeGUI(root, n)
root.mainloop()
