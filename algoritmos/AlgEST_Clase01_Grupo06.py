# AlgEST_Clase01_Grupo06.py

import time
from algoritmos.fun_alg_evolutivos import *


class Estacionario:
    def __init__(self, matriz_distancias, params, logger=None):
        self.matriz_distancias = matriz_distancias
        self.p = params
        self.logger = logger

        self.num_evaluaciones = 0
        self.inicio_tiempo = None
        self.tiempo_ejecucion = None
        self.generacion = 1
        self.poblacion = []
        self.cruce = cruce_ox2 if self.p['cruce'] == 'OX2' else cruce_moc


    def inicializar_poblacion(self) -> list[Individuo]:
        return inicializar_poblacion(self.p['tamanio'], self.p['per_individuos'], self.p['k'],
                                     self.matriz_distancias, self.generacion)

    def seleccion(self) -> list[Individuo]:
        return seleccion(self.poblacion, 2, self.p['kBest'])


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo estacionario."""

        self.inicio_tiempo = time.time()
        self.poblacion = self.inicializar_poblacion()
        self.num_evaluaciones += len(self.poblacion)

        # --------------------------------LOGGING---------------------------------------#
        self.logger.registrar_evento('Iniciando ejecución del algoritmo estacionario')
        self.logger.registrar_evento('=== Inicio de la Generación 0 ===')
        self.logger.registrar_evento('Población inicial generada:')
        for idx, individuo in enumerate(self.poblacion, start=1):
            self.logger.registrar_evento(f'  Individuo: {idx}  {individuo}')
        # --------------------------------LOGGING---------------------------------------#

        while (self.num_evaluaciones < self.p['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.p['tiempo']):
            self.generacion += 1

            # Genera dos hijos y colocalos en la poblacion por torneo de perdedores
            padres = self.seleccion()
            hijos = self.cruce(padres[0], padres[1], self.generacion)
            self.num_evaluaciones += 2

            for hijo in hijos:
                if random.random() < self.p['per_mutacion']:
                    hijo.intercambio_2opt(self.generacion)
                    self.num_evaluaciones += 1

            self.reemplazamiento(hijos[0], hijos[1])

            # --------------------------------LOGGING---------------------------------------#
            if self.generacion == 1:
                self.logger.registrar_evento(f'\nPadres seleccionados: {[p for p in padres]}')
                self.logger.registrar_evento(f'\nHijos obtenidos: {[h for h in hijos]}\n')
            
            self.logger.registrar_evento(f'\nGeneración {self.generacion}: Nuevos individuos generados:')
            for ixz, individuo in enumerate(hijos, start=1):
                self.logger.registrar_evento(f"  Individuo: {ixz}  {individuo}")
            self.logger.registrar_evento(
                f'Evaluaciones realizadas hasta ahora: {self.num_evaluaciones} '
                f'| Mejor fitness actual: {min(ind.fitness for ind in self.poblacion):.2f}'
            )
            # --------------------------------LOGGING---------------------------------------#

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo
        self.logger.cerrar_log()

    def reemplazamiento(self, hijo1: Individuo, hijo2: Individuo):
        """Elimina dos indiviuos de la población y coloca a los hijos"""
        torneo1 = random.sample(range(len(self.poblacion)), self.p['kWorst'])
        peor_individuo1 = max(torneo1, key=lambda i: self.poblacion[i].fitness)

        while True:
            torneo2 = random.sample(range(len(self.poblacion)), self.p['kWorst'])
            peor_individuo2 = max(torneo1, key=lambda i: self.poblacion[i].fitness)
            if peor_individuo2 != peor_individuo1:
                break

        self.poblacion[peor_individuo1] = hijo1
        self.poblacion[peor_individuo2] = hijo2