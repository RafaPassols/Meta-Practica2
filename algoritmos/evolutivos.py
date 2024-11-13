# algoritmos/evolutivosevolutivos.py

# Importaciones de bibliotecas estándar
import random, time
from typing import Callable

from numpy.ma.core import append

# Importaciones locales
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio
from auxiliares.individuo import Individuo

# Importaciones de tercero
import numpy as np


class Generacional:
    """Implementa un algoritmo evolutivo generacional (GEN)."""

    def __init__(self, matriz_distancias, params):
        self.matriz_distancias = matriz_distancias
        self.p = params

        self.num_evaluaciones = 0
        self.inicio_tiempo = None
        self.tiempo_ejecucion = None

        self.generacion = 1
        self.poblacion = []
        self.elites = []
        self.cruce = cruce_ox2 if (params['cruce'] == 'OX2') else cruce_moc


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo generacional."""
        self.inicio_tiempo = time.time()
        self.inicializar_poblacion()
        self.num_evaluaciones += len(self.poblacion)

        while (self.num_evaluaciones < self.p['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.p['tiempo']):
            self.generacion += 1

            # Se guardan las mejores soluciones
            self.elites = sorted(self.poblacion, key=lambda ind: ind.distancia)[:self.p['E']]

            # Selecciona aquellos individuos que tienen una posibilidad de cruzarse
            supervivientes = self.seleccion()

            # Recombina algunos individuos de los seleccionados y crea la poblacion intermedia
            hijos = []
            for i in range(0, len(supervivientes) - 1, 2):
                if random.random() < self.p['per_cruce']:
                    hijos.extend(self.cruce(supervivientes[i], supervivientes[i+1]))
            self.num_evaluaciones += len(hijos)
            poblacion_intermedia = supervivientes + hijos

            # Aplica o no una mutación a cada individuo de la población intermedia
            for individuo in poblacion_intermedia:
                if random.random() < self.p['per_mutacion']:
                    individuo.mutar()
                    self.num_evaluaciones += 1

            self.poblacion = self.reemplazamiento(poblacion_intermedia)

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo

    def inicializar_poblacion(self):
        self.poblacion = inicializar_poblacion(self.p['tamanio'], self.p['per_individuos'],
                                               self.p['k'], self.matriz_distancias)
    def seleccion(self) -> list[Individuo]:
        """Escoge N individuos de una población según un torneo aleatorio de tamaño k"""
        return seleccion(self.poblacion, len(self.poblacion), self.p['kBest'])

    def reemplazamiento(self, poblacion: list[Individuo]) -> list[Individuo]:
        """
        Devuelve nueva población formada por los n mejores de poblacion. Si se proporcionan elites entonces
        se garantiza que serán parte de la nueva población a través de un torneo de perdedores de k individuos
        """
        # Tomamos los n mejores
        nueva_poblacion = sorted(poblacion, key=lambda i : i.distancia)[:len(self.poblacion)]

        if self.elites is not None:
            if self.p['kWorst'] < 0:
                ValueError("reemplazamiento_generacional(): k debe ser > 0 si elites != None")

            nuevos_individuos = set(nueva_poblacion)
            for elite in self.elites:
                if elite not in nuevos_individuos:
                    # Realizar el torneo para elegir un peor individuo
                    torneo = random.sample(nueva_poblacion, self.p['kWorst'])
                    peor_individuo = max(torneo, key=lambda individuo: individuo.distancia)

                    # Reemplazar al peor individuo por el individuo élite
                    nueva_poblacion.remove(peor_individuo)
                    nueva_poblacion.append(elite)
        return nueva_poblacion

class Estacionario:
    def __init__(self, matriz_distancias, params):
        self.matriz_distancias = matriz_distancias
        self.p = params

        self.num_evaluaciones = 0
        self.inicio_tiempo = None
        self.tiempo_ejecucion = None
        self.generacion = 1
        self.poblacion = []
        self.cruce = cruce_ox2 if self.p['cruce'] == 'OX2' else cruce_moc
        

    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo estacionario."""
        self.inicio_tiempo = time.time()
        self.inicializar_poblacion()
        self.num_evaluaciones += len(self.poblacion)

        while (self.num_evaluaciones < self.p['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.p['tiempo']):
            # print(f'GENERACION = {self.generacion} - EVALUACIONES = {self.num_evaluaciones}')
            self.generacion += 1

            # Genera dos hijos y colocalos en la poblacion por torneo de perdedores
            padres = self.seleccion()
            hijos = self.cruce(padres[0], padres[1])
            self.num_evaluaciones += 2

            for hijo in hijos:
                if random.random() < self.p['per_mutacion']:
                    hijo.mutar()
                    self.num_evaluaciones += 1

            self.reemplazamiento(hijos[0], hijos[1])

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo

    def inicializar_poblacion(self):
        self.poblacion = inicializar_poblacion(self.p['tamanio'], self.p['per_individuos'],
                                               self.p['k'], self.matriz_distancias)

    def seleccion(self) -> list[Individuo]:
        """Escoge 2 individuos de una población según un torneo aleatorio de tamaño k"""
        return seleccion(self.poblacion, 2, self.p['kWorst'])

    def reemplazamiento(self, hijo1: Individuo, hijo2: Individuo):
        """Elimina dos indiviuos de la población y coloca a los hijos"""
        for hijo in [hijo1, hijo2]:
            torneo = random.sample(range(len(self.poblacion)), self.p['kWorst'])
            peor_individuo = max(torneo, key=lambda i: self.poblacion[i].distancia)
            self.poblacion[peor_individuo] = hijo



def inicializar_poblacion(tam: int, factor_aleatorio: float, k_greedy: int, matriz_distancias: list[list[float]]) -> list[Individuo]:
    """Genera una población utilizando aleatoriedad y el algoritmo de Greedy aleatorio
    :param tam: tamaño de la población a devolver
    :param factor_aleatorio: proporción de individuos a generar aleatoriamente. Los individuos a generar mediante
    Greedy aleatorio serán de (1-factor_aleatorio)
    :param k_greedy: parámetro del algoritmo greedy, cuanto más alto más aleatorio
    :param matriz_distancias: matriz que representa la distancia entre las ciudades
    :return: lista de tam individuos
    """
    poblacion = [None] * tam
    num_individuos_aleatoria = int(tam * factor_aleatorio)

    # Generación aleatoria
    for i in range(num_individuos_aleatoria):
        tour = np.random.default_rng().permutation(len(matriz_distancias))
        poblacion[i] = Individuo(tour, matriz_distancias)

    # Generación greedy aleatorio
    for i in range(num_individuos_aleatoria, tam):
        greedy = GreedyAleatorio(matriz_distancias, k_greedy)
        tour, distancia = greedy.ejecutar()
        poblacion[i] = Individuo(tour, matriz_distancias, distancia)

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
        torneo = random.sample(poblacion, k)
        mejor_individuo = min(torneo, key=lambda individuo: individuo.distancia)
        seleccionados.append(mejor_individuo)
    return seleccionados

def cruce_ox2(padre1: Individuo, padre2: Individuo) -> tuple[Individuo, Individuo]:
    """Aplica el cruce OX2 entre dos padres para generar dos hijos
    :return: tupla con dos hijos"""

    # Elegir n/2 posiciones aleatorias de padre2 ordenadas
    num_ciudades = len(padre1.tour)
    num_posiciones = int(num_ciudades/2)
    posiciones = np.random.default_rng().choice(num_ciudades, size=num_posiciones, replace=False)
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
    hijo1 = Individuo(hijo1_tour, padre1.matriz_distancias)  # El fitness se calcula automáticamente
    hijo2_tour = padre2.tour.copy()
    hijo2_tour[posiciones_e1_en_p2] = elementos_p1
    hijo2 = Individuo(hijo2_tour, padre2.matriz_distancias)

    return hijo1, hijo2

def cruce_moc(padre1: Individuo, padre2: Individuo) -> tuple[Individuo, Individuo]:
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
    hijo1 = Individuo(hijo1_tour, padre1.matriz_distancias)  # El fitness se calcula automáticamente
    hijo2_tour = padre2.tour.copy()
    hijo2_tour[posiciones_e1_en_p2] = elementos_p1
    hijo2 = Individuo(hijo2_tour, padre2.matriz_distancias)

    return hijo1, hijo2
