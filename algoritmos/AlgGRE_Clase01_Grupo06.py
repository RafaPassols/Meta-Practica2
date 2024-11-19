# AlgGRE_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random

# Importaciones de terceros
import numpy as np


class GreedyAleatorio:
    """Implementa el algoritmo greedy aleatorio para la generación de soluciones"""

    def __init__(self, matriz, k):
        self.matriz = matriz
        self.k = k

        if not (1 <= k <= self.matriz.shape[0]):
            raise ValueError("El valor de 'k' debe estar entre 1 y el número total de ciudades.")


    def ejecutar(self):
        tour = []
        num_ciudades = self.matriz.shape[0]
        visitadas = np.zeros(num_ciudades, dtype=bool)
        rng = np.random.default_rng()

        # Calcula la suma de cada ciudad al resto
        suma_distancias = np.sum(self.matriz, axis=1)

        # Ordena las ciudades
        ciudades_ordenadas = np.argsort(suma_distancias)

        # Selecciona la ciudad inicial de entre las 'k' más prometedoras
        prometedoras = ciudades_ordenadas[:self.k]
        ciudad_actual = rng.choice(prometedoras)

        # Añade la ciudad a la solucion
        tour.append(ciudad_actual)
        visitadas[ciudad_actual] = True
        distancia_total = 0.0

        for _ in range(num_ciudades - 1):
            # Filtra las ciudades no visitadas y obtiene las 'k' más prometedoras
            no_visitadas = ciudades_ordenadas[~visitadas[ciudades_ordenadas]]
            prometedoras = no_visitadas[:self.k]

            # Elige una ciudad aleatoriamente
            ciudad_siguiente = rng.choice(prometedoras)
            distancia_total += self.matriz[ciudad_actual, ciudad_siguiente]

            # Actualiza la solución
            tour.append(ciudad_siguiente)
            visitadas[ciudad_siguiente] = True
            ciudad_actual = ciudad_siguiente

        # Regreso a la ciudad de inicio
        distancia_total += self.matriz[ciudad_actual, tour[0]]

        # Convierte tour a un array de numpy
        tour = np.asarray(tour)

        return tour, distancia_total