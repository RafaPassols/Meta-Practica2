# modelos/individuo.py

# Importaciones locales
from auxiliares.funciones_generales import factorizacion_2opt

# Importaciones de terceros
import numpy as np


class Individuo:
    """Implementa un individuo de la población."""

    def __init__(self, tour, matriz_distancias, distancia=None):
        self.tour = tour
        self.matriz_distancias = matriz_distancias
        self.distancia = self.calcular_distancia() if distancia is None else distancia


    def calcular_distancia(self) -> float:
        """Calcula la distancia total de un tour."""
        return (np.sum(self.matriz_distancias[self.tour[:-1], self.tour[1:]]) +
                self.matriz_distancias[self.tour[-1], self.tour[0]])


    def mutar(self):
        """Realiza una mutación (2-opt) en el individuo."""
        n = len(self.tour)
        i, j = np.random.default_rng().choice(n, size=2, replace=False)
        self.distancia += factorizacion_2opt(self.tour, self.matriz_distancias, i, j)
        self.tour[i], self.tour[j] = self.tour[j], self.tour[i]


    def __repr__(self):
        return f'distancia={self.distancia}'