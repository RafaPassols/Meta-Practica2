# modelos/individuo.py

# Importaciones de tercero
import numpy as np


class Individuo:
    """Implementa un individuo (solución) de la población."""

    def __init__(self, tour):
        self.tour = tour
        self.fitness = 0
        self.flag = False
        self.generacion = -1    # Como la inicializo (¿por cabecera?)


    def intercambio_2_opt(self, matriz):
        """Aplica el operador de intercambio 2-opt."""

        n = len(self.tour)
        i, j = np.random.choice(range(1, n - 1), size=2, replace=False) # Evita el primer y último índice

        arcos_desaparecen, arcos_nuevos = self.factorizacion(matriz, i, j)
        nuevo_fitness = self.fitness - arcos_desaparecen + arcos_nuevos

        # Actualizo el tour y el fitness
        self.tour[i], self.tour[j] = self.tour[j], self.tour[i]
        self.fitness = nuevo_fitness


    def factorizacion(self, matriz, i, j):
        """Calcula eficientemente la distancia de un tour tras el intercambio 2-opt."""

        n = len(self.tour)
        tour = self.tour

        # Manejar el caso cuando las ciudades son consecutivas
        if abs(i - j) == 1 or (i == 0 and j == n - 1) or (i == n - 1 and j == 0):
            arcos_desaparecen = matriz[tour[i - 1], tour[i]] + matriz[tour[j], tour[(j + 1) % n]]
            arcos_nuevos = matriz[tour[i - 1], tour[j]] + matriz[tour[i], tour[(j + 1) % n]]
        else:
            arcos_desaparecen = (
                    matriz[tour[i - 1], tour[i]] + matriz[tour[i], tour[(i + 1) % n]] +
                    matriz[tour[j - 1], tour[j]] + matriz[tour[j], tour[(j + 1) % n]]
            )
            arcos_nuevos = (
                    matriz[tour[i - 1], tour[j]] + matriz[tour[j], tour[(i + 1) % n]] +
                    matriz[tour[j - 1], tour[i]] + matriz[tour[i], tour[(j + 1) % n]]
            )

        return arcos_desaparecen, arcos_nuevos


    def __repr__(self):
        return f'fitness: {self.fitness:.2f}'