# algoritmos/AlgEST_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.individuo import Individuo
from auxiliares.funciones_generales import funcion_objetivo, cruce_ox2, cruce_moc
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio

# Importaciones de tercero
import numpy as np


class Estacionario:
    """Implementa el algoritmo evolutivo estacionario (EST)."""

    def __init__(self, matriz, params):
        self.matriz = matriz
        self.params = params
        self.generacion = None
        self.poblacion = []     # Lista de individuos (soluciones)

        self.evaluaciones = 0   # Evaluaciones realizadas
        self.elite = []         # Almacena el individuo élite (depende de 'E')

        self.inicio_tiempo = time.time()
        self.tiempo_ejecucion = None


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo estacionario."""

        self.generacion = 0
        self.inicializar_poblacion()
        self.evaluar(self.poblacion)

        while (self.evaluaciones < self.params['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.params['tiempo']):

            # t = t+1
            self.generacion += 1

            # Selecciona dos padres de la población P(t-1)
            padres = self.seleccionar()

            # Recombina los padres para obtener los hijos
            hijos = self.recombinar(padres)

            # Se mutan los hijos generados en el paso anterior
            self.mutar(hijos)

            # Evalúa los nuevos individuos generados
            self.evaluar(hijos)

            # Reemplaza los peores individuos de la población por los hijos
            self.reemplazar(hijos)

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo


    def inicializar_poblacion(self):
        """Inicializa la población de individuos."""

        num_individuos_aleatoria = int(self.params['tamanio'] * self.params['per_individuos'])
        num_individuos_greedy = self.params['tamanio'] - num_individuos_aleatoria

        # Generación aleatoria
        for _ in range(num_individuos_aleatoria):
            tour = np.random.default_rng().permutation(len(self.matriz))
            individuo = Individuo(tour)
            self.poblacion.append(individuo)

        # Generación greedy aleatorio
        for _ in range(num_individuos_greedy):
            greedy = GreedyAleatorio(self.matriz, self.params)
            tour = greedy.ejecutar()
            individuo = Individuo(tour)
            self.poblacion.append(individuo)


    def evaluar(self, poblacion):
        """Evalúa cada individuo no evaluado de la población."""

        for individuo in poblacion:
            # Si el individuo no ha sido evaluado
            if not individuo.flag:
                # Evaluamos el individuo (solución) calculando su fitness
                individuo.fitness = funcion_objetivo(individuo.tour, self.matriz)
                individuo.flag = True
                self.evaluaciones += 1


    def seleccionar(self):
        """Operador de selección basado en un torneo binario con kBest."""

        padres = []

        while True:
            torneo_1 = random.sample(self.poblacion, self.params['kBest'])
            torneo_2 = random.sample(self.poblacion, self.params['kBest'])

            # Selecciona el mejor individuo de cada torneo
            padre_1 = min(torneo_1, key=lambda ind: ind.fitness)
            padre_2 = min(torneo_2, key=lambda ind: ind.fitness)

            # Asegura que los padres seleccionados sean distintos
            if padre_1 != padre_2:
                padres.append(padre_1)
                padres.append(padre_2)
                break

        return padres


    def recombinar(self, padres):
        """Cruza los padres seleccionados con una probabilidad del 100%."""

        hijos = []

        if self.params['cruce'] == 'OX2':
            hijo_1, hijo_2 = cruce_ox2(padres[0], padres[1])
        else:
            hijo_1, hijo_2 = cruce_moc(padres[0], padres[1])

        # Establezco la generación en que fueron generados
        hijo_1.generacion = self.generacion
        hijo_2.generacion = self.generacion

        hijos.append(hijo_1)
        hijos.append(hijo_2)

        return hijos


    def mutar(self, nueva_poblacion):
        """Aplica la mutación con una cierta probabilidad a cada individuo de la población."""

        for individuo in nueva_poblacion:
            if random.random() < self.params['per_mutacion']:
                # Muta al individuo (aplica 2-opt)
                individuo.intercambio_2_opt(self.matriz)


    def reemplazar(self, hijos):
        """Reemplaza a los dos peores individuos de la población."""

        # Repetimos hasta realizar todos los reemplazamientos
        for hijo in hijos:

            while True:
                torneo = random.sample(self.poblacion, self.params['kWorst'])
                # Nos aseguramos que ambos individuos sean distintos
                if len(torneo) == len(set(torneo)):
                    break

            peor = max(torneo, key=lambda ind: ind.fitness)

            # Reemplazo
            self.poblacion.remove(peor)
            self.poblacion.append(hijo)