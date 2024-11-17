# algoritmos/AlgGRE_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random

# Importaciones de terceros
import numpy as np


class GreedyAleatorio:
    """Implementa el algoritmo greedy aleatorio."""

    def __init__(self, matriz, params):
        self.matriz = matriz
        self.params = params

        if 'k' not in self.params:
            raise ValueError("El parámetro 'k' debe estar definido en los parámetros.")
        if not (1 <= self.params['k'] <= self.matriz.shape[0]):
            raise ValueError("El valor de 'k' debe estar entre 1 y el número total de ciudades.")


    def ejecutar(self):
        """Ejecuta el algoritmo greedy aleatorio."""

        num_ciudades = self.matriz.shape[0]

        tour = []
        visitadas = np.zeros(num_ciudades, dtype=bool)

        # Calcula la suma de cada ciudad al resto
        suma_distancias = np.sum(self.matriz, axis=1)

        # Ordena las ciudades
        ciudades_ordenadas = np.argsort(suma_distancias)

        # Selecciona la ciudad inicial de entre las 'k' más prometedoras
        prometedoras = ciudades_ordenadas[:self.params['k']]
        ciudad_actual = random.choice(prometedoras)

        # Añade la ciudad a la solucion
        tour.append(ciudad_actual)
        visitadas[ciudad_actual] = True

        for _ in range(num_ciudades - 1):
            # Filtra las ciudades no visitadas y obtiene las 'k' más prometedoras
            no_visitadas = ciudades_ordenadas[~visitadas[ciudades_ordenadas]]
            prometedoras = no_visitadas[:self.params['k']]

            # Elige una ciudad aleatoriamente
            ciudad_siguiente = random.choice(prometedoras)

            # Actualiza la solución
            tour.append(ciudad_siguiente)
            visitadas[ciudad_siguiente] = True

        # Convierte tour a un array de numpy
        tour = np.asarray(tour)

        return tour