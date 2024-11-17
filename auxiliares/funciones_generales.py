# auxiliares/funciones_generales.py

# Importaciones de bibliotecas estándar
import random

# Importaciones locales
from modelos.individuo import Individuo

# Importaciones de tercero
import numpy as np


def generar_semillas(dni_alumno, num_semillas, offset=0):
    """Genera un número de semillas pseudoaleatorias"""

    if not isinstance(num_semillas, int) or num_semillas <= 0:
        raise ValueError("num_semillas debe ser un entero positivo.")

    random.seed(dni_alumno + offset)
    semillas = [random.randint(1, 100000) for _ in range(num_semillas)]

    return semillas


def funcion_objetivo(tour, matriz):
    """Calcula la distancia (fitness) del individuo (solución)."""

    distancia = np.sum(matriz[tour[:-1], tour[1:]]) + matriz[tour[-1], tour[0]]
    return distancia


def cruce_ox2(padre1, padre2):
    """Aplica el cruce OX2 entre dos padres para generar un hijo."""

    n = len(padre1.tour)

    # Elegir al azar varias posiciones
    num_posiciones = random.randint(1, max(1, n // 3))  # Selecciona aproximadamente el 33% del tour
    posiciones = np.random.choice(range(n), size=num_posiciones, replace=False)
    posiciones.sort()

    # Seleccionamos los elementos en esas posiciones
    elementos_p1 = padre1.tour[posiciones]
    elementos_p2 = padre2.tour[posiciones]

    # Localizamos las posiciones que ocupan esos elementos en padre1
    posiciones_e2_en_p1 = np.where(np.isin(padre1.tour, elementos_p2))
    posiciones_e1_en_p2 = np.where(np.isin(padre2.tour, elementos_p1))

    # Crea un nuevo individuo hijo y completa con los elementos no repetidos de padre2 y viceversa
    hijo1_tour = padre1.tour.copy()
    hijo1_tour[posiciones_e2_en_p1] = elementos_p2
    hijo1 = Individuo(hijo1_tour)  # El fitness se calcula automáticamente

    hijo2_tour = padre2.tour.copy()
    hijo2_tour[posiciones_e1_en_p2] = elementos_p1
    hijo2 = Individuo(hijo2_tour)  # El fitness se calcula automáticamente

    return hijo1, hijo2


def cruce_moc(padre1, padre2):
    """Aplica el cruce MOC entre dos padres para generar un hijo."""

    n = len(padre1.tour)

    # Elegir un punto de cruce al azar
    punto_cruce = random.randint(1, n - 2)  # Se elige el punto evitando los extremos

    # Identifica la mitad derecha de padre2
    mitad_der_padre2 = padre2.tour[punto_cruce:]
    mitad_der_padre1 = padre1.tour[punto_cruce:]

    # Verificar si cada elemento de padre1 está en mitad_der_padre2
    esta_en_padre2 = np.isin(padre1.tour, mitad_der_padre2)
    indices_padre1 = np.where(esta_en_padre2)[0]    # índices de los elementos de padre1 que están en padre2

    esta_en_padre1 = np.isin(padre2.tour, mitad_der_padre1)
    indices_padre2 = np.where(esta_en_padre1)[0]    # índices de los elementos de padre2 que están en padre1

    # Completa las posiciones '*' con los elementos de la mitad derecha de padre2 y viceversa
    hijo1_tour = padre1.tour.copy()
    hijo1_tour[indices_padre1] = mitad_der_padre2
    hijo1 = Individuo(hijo1_tour)  # El fitness se calcula automáticamente

    hijo2_tour = padre2.tour.copy()
    hijo2_tour[indices_padre2] = mitad_der_padre1
    hijo2 = Individuo(hijo2_tour)  # El fitness se calcula automáticamente

    return hijo1, hijo2