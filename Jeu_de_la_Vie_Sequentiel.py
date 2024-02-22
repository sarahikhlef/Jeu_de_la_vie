import numpy as np
import random
import time


# Fonction pour initialiser la matrice de manière aléatoire
def init_matrix(n):
    # Premier tableau (n+2)x(n+2) qui va contenir les cellules
    matrix = [[0] * (n + 2) for _ in range(n + 2)]

    for _ in range(random.randint(n, n * n)):
        i, j = random.randint(1, n), random.randint(1, n)
        matrix[i][j] = 1

    return matrix


# Fonction pour compter le nombre de voisins de chaque cellule
def count_neighbors(matrix, n):
    # Deuxième tableau (n+2)x(n+2) utilisé pour stocker le nombre de cellules voisines occupées.
    neighbors = [[0] * (n + 2) for _ in range(n + 2)]

    for i in range(1, n-1):
        for j in range(1, n-1):
            neighbors[i][j] = sum([matrix[i + 1][j],
                                   matrix[i - 1][j],
                                   matrix[i][j + 1],
                                   matrix[i][j - 1],
                                   matrix[i + 1][j + 1],
                                   matrix[i - 1][j - 1],
                                   matrix[i + 1][j - 1],
                                   matrix[i - 1][j + 1]])
    return neighbors


# Fonction pour évoluer la matrice d'une génération à l'autre
def evolution(matrix):
    new_matrix = np.copy(matrix)
    neighbors = count_neighbors(matrix, len(matrix))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if matrix[i][j] == 0:
                if neighbors[i][j] == 3:
                    new_matrix[i][j] = 1
            else:
                if neighbors[i][j] in (2, 3):
                    new_matrix[i][j] = 1
                else:
                    new_matrix[i][j] = 0
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
        matrix = evolution(matrix)


main()
