import numpy as np
import random
import time
import threading


# Fonction pour initialiser la matrice de manière aléatoire
def init_matrix(n):
    # Premier tableau (n+2)x(n+2) qui va contenir les cellules
    matrix = [[0] * (n + 2) for _ in range(n + 2)]

    for _ in range(random.randint(n, n * n)):
        i, j = random.randint(1, n), random.randint(1, n)
        matrix[i][j] = 1

    return matrix


# Fonction pour évoluer une cellule spécifique de la matrice
def evolution(i, j, matrix, new_matrix):
    nb_neighbors = sum([matrix[i + 1][j],
                       matrix[i - 1][j],
                       matrix[i][j + 1],
                       matrix[i][j - 1],
                       matrix[i + 1][j + 1],
                       matrix[i - 1][j - 1],
                       matrix[i + 1][j - 1],
                       matrix[i - 1][j + 1]])

    if matrix[i][j] == 0:
        if nb_neighbors == 3:
            new_matrix[i][j] = 1
    else:
        if nb_neighbors in (2, 3):
            new_matrix[i][j] = 1
        else:
            new_matrix[i][j] = 0


# Fonction pour évoluer la matrice en parallèle en utilisant des threads indépendants
def evolution_threads(matrix):
    new_matrix = np.copy(matrix)
    threads = []
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            thread = threading.Thread(target=evolution, args=(i, j, matrix, new_matrix))
            thread.start()
            threads.append(thread)

    # Attendre que tous les threads se terminent
    for i in range(0, len(threads)):
        threads[i].join()

    return new_matrix


# Fonction pour afficher la matrice
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))
    print()


def main():
    n = int(input("Saisir n: "))
    nb_generations = int(input("Saisir le nombre de generations: "))

    matrix = init_matrix(n)

    for i in range(nb_generations):
        print(f"Generation {i + 1}:")
        print_matrix(matrix)
        time.sleep(1)
        matrix = evolution_threads(matrix)


main()
