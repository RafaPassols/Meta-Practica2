# modelos/individuo.py
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


    def intercambio_2opt(self):
        """Realiza una mutación (2-opt) en el individuo."""
        n = len(self.tour)
        i, j = np.random.default_rng().choice(n, size=2, replace=False)
        self.distancia += factorizacion_2opt(self.tour, self.matriz_distancias, i, j)
        self.tour[i], self.tour[j] = self.tour[j], self.tour[i]

    def __repr__(self):
        return f'distancia={self.distancia}'


def factorizacion_2opt(tour, m, i, j) -> float:
    """
        Calcula la diferencia en distancia de un tour si se realizase un 2-opt en las posiciones (i,j)
        Parameters:
        - tour: permutación de ciudades
        - m: matriz de distancias
        . i,j: posiciones intercambiadas
    """
    n = len(tour)
    i, j = min(i, j), max(i, j)
    if j - i == 1 or (i == 0 and j == n - 1):
        # Ciudades consecutivas
        arcos_desaparecen = m[tour[i - 1], tour[i]] + m[tour[j], tour[(j + 1) % n]]
        arcos_nuevos = m[tour[i - 1], tour[j]] + m[tour[i], tour[(j + 1) % n]]
    else:
        arcos_desaparecen = (
                m[tour[i - 1], tour[i]] + m[tour[i], tour[(i + 1) % n]] +
                m[tour[j - 1], tour[j]] + m[tour[j], tour[(j + 1) % n]]
        )
        arcos_nuevos = (
                m[tour[i - 1], tour[j]] + m[tour[j], tour[(i + 1) % n]] +
                m[tour[j - 1], tour[i]] + m[tour[i], tour[(j + 1) % n]]
        )

    return arcos_nuevos - arcos_desaparecen