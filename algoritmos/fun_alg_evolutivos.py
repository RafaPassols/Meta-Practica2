# fun_alg_evolutivos.py

# Importaciones de bibliotecas estándar
import random

# Importaciones locales
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio
from modelos.individuo import Individuo

# Importaciones de tercero
import numpy as np


def inicializar_poblacion(tam: int, factor_aleatorio: float, k_greedy: int,
                          matriz_distancias: list[list[float]], generacion: int) -> list[Individuo]:
    """Genera una población utilizando aleatoriedad y el algoritmo de Greedy aleatorio
    :param tam: tamaño de la población a devolver
    :param factor_aleatorio: proporción de individuos a generar aleatoriamente. Los individuos a generar mediante
    Greedy aleatorio serán de (1-factor_aleatorio)
    :param k_greedy: parámetro del algoritmo greedy, cuanto más alto más aleatorio
    :param matriz_distancias: matriz que representa la distancia entre las ciudades
    :return: lista de tam individuos
    """
    poblacion = []
    num_individuos_aleatoria = int(tam * factor_aleatorio)

    # Generación aleatoria
    for i in range(num_individuos_aleatoria):
        tour = np.random.default_rng().permutation(len(matriz_distancias))
        poblacion.append(Individuo(tour, matriz_distancias, generacion))

    # Generación greedy aleatorio
    for i in range(num_individuos_aleatoria, tam):
        greedy = GreedyAleatorio(matriz_distancias, k_greedy)
        tour, distancia = greedy.ejecutar()
        poblacion.append(Individuo(tour, matriz_distancias, generacion, distancia))

    return poblacion

def seleccion(poblacion: list[Individuo], s: int, k: int) -> list[Individuo]:
    """ Escoge s individuos de una población según un torneo aleatorio de tamaño k
    :param poblacion: Lista de individuos
    :param s: Número de individuos a devolver
    :param k: Tamaño del torneo
    :return: Lista de individuos de tamaño s
    """
    seleccionados = []
    for _ in range(s):
        # El torneo debe hacerse con individuos únicos
        while True:
            # random.sample es bueno cuando k << len(poblacion)
            torneo = random.sample(poblacion, k)
            if len(torneo) == len(set(torneo)):
                break

        mejor_individuo = min(torneo, key=lambda individuo: individuo.fitness)
        seleccionados.append(mejor_individuo)

    return seleccionados

def cruce_ox2(padre1: Individuo, padre2: Individuo, generacion: int) -> tuple[Individuo, Individuo]:
    """Aplica el cruce OX2 entre dos padres para generar dos hijos
    :return: tupla con dos hijos"""

    # Elegir n/2 posiciones aleatorias de padre2 ordenadas
    num_ciudades = len(padre1.tour)
    num_posiciones = int(num_ciudades/2)
    posiciones = np.random.default_rng().choice(num_ciudades, size=num_posiciones, replace=False, shuffle=False)
    posiciones.sort()

    # Seleccionamos los elementos en esas posiciones
    elementos_p1 = padre1.tour[posiciones]
    elementos_p2 = padre2.tour[posiciones]

    # Localizamos las posiciones que ocupan esos elementos en el otro padre
    posiciones_e2_en_p1 = np.nonzero(np.isin(padre1.tour, elementos_p2))
    posiciones_e1_en_p2= np.nonzero(np.isin(padre2.tour, elementos_p1))

    # Crea un hijo copia de un padre pero con los elementos seleccionados en el orden del otro
    hijo1_tour = padre1.tour.copy()
    hijo1_tour[posiciones_e2_en_p1] = elementos_p2
    hijo1 = Individuo(hijo1_tour, padre1.matriz_distancias, generacion)  # El fitness se calcula automáticamente
    hijo2_tour = padre2.tour.copy()
    hijo2_tour[posiciones_e1_en_p2] = elementos_p1
    hijo2 = Individuo(hijo2_tour, padre2.matriz_distancias, generacion)

    return hijo1, hijo2

def cruce_moc(padre1: Individuo, padre2: Individuo, generacion: int) -> tuple[Individuo, Individuo]:
    """Aplica el cruce MOC entre dos padres para generar dos hijos
    :return: tupla con dos hijos"""
    num_ciudades = len(padre1.tour)

    # Elegir un punto de cruce al azar evitando los extremos
    punto_cruce = random.randint(1, num_ciudades - 2)

    # Identificamos las dos partes
    elementos_p1 = padre1.tour[:punto_cruce]
    elementos_p2 = padre2.tour[punto_cruce:]

    # índices de los elementos un padre que están en el otro
    posiciones_e2_en_p1 = np.nonzero(np.isin(padre1.tour, elementos_p2))
    posiciones_e1_en_p2 = np.nonzero(np.isin(padre2.tour, elementos_p1))

    # Crea un hijo copia de un padre pero con los elementos seleccionados en el orden del otro
    hijo1_tour = padre1.tour.copy()
    hijo1_tour[posiciones_e2_en_p1] = elementos_p2
    hijo1 = Individuo(hijo1_tour, padre1.matriz_distancias, generacion)  # El fitness se calcula automáticamente
    hijo2_tour = padre2.tour.copy()
    hijo2_tour[posiciones_e1_en_p2] = elementos_p1
    hijo2 = Individuo(hijo2_tour, padre2.matriz_distancias, generacion)

    return hijo1, hijo2
