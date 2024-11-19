import time
from algoritmos.fun_alg_evolutivos import *


class Generacional:
    """Implementa un algoritmo evolutivo generacional (GEN)."""

    def __init__(self, matriz_distancias, params, logger=None):
        self.matriz_distancias = matriz_distancias
        self.p = params
        self.logger = logger

        self.num_evaluaciones = 0
        self.inicio_tiempo = None
        self.tiempo_ejecucion = None

        self.generacion = 1
        self.poblacion = []
        self.elites = []
        self.cruce = cruce_ox2 if (params['cruce'] == 'OX2') else cruce_moc


    def inicializar_poblacion(self) -> list[Individuo]:
        return inicializar_poblacion(self.p['tamanio'], self.p['per_individuos'], self.p['k'],
                                     self.matriz_distancias, self.generacion)

    def seleccion(self) -> list[Individuo]:
        return seleccion(self.poblacion, len(self.poblacion), self.p['kBest'])


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo generacional."""

        self.inicio_tiempo = time.time()
        self.poblacion = self.inicializar_poblacion()
        self.num_evaluaciones += len(self.poblacion)

        # --------------------------------LOGGING---------------------------------------#
        self.logger.registrar_evento('Iniciando ejecución del algoritmo generacional.')
        self.logger.registrar_evento('Población inicial generada:')
        for idx, individuo in enumerate(self.poblacion, start=1):
            self.logger.registrar_evento(f'  Individuo: {idx}  {individuo}')
            self.logger.registrar_evento('=== Inicio de la Generación 0 ===')
        # --------------------------------LOGGING---------------------------------------#

        while (self.num_evaluaciones < self.p['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.p['tiempo']):
            self.generacion += 1

            # Se guardan las mejores soluciones
            self.elites = sorted(self.poblacion, key=lambda ind: ind.fitness)[:self.p['E']]

            # Selecciona aquellos individuos que tienen una posibilidad de cruzarse
            padres = self.seleccion()

            # Recombina algunos individuos de los seleccionados y crea la poblacion intermedia
            hijos = []
            for i in range(0, len(padres) - 1, 2):
                if random.random() < self.p['per_cruce']:
                    hijos.extend(self.cruce(padres[i], padres[i+1], self.generacion))
            self.num_evaluaciones += len(hijos)
            poblacion_intermedia = padres + hijos

            # Aplica o no una mutación a cada individuo de la población intermedia
            for individuo in poblacion_intermedia:
                if random.random() < self.p['per_mutacion']:
                    individuo.intercambio_2opt(self.generacion)
                    self.num_evaluaciones += 1

            self.poblacion = self.reemplazamiento(poblacion_intermedia)

            # --------------------------------LOGGING---------------------------------------#
            if self.generacion == 1:
                self.logger.registrar_evento(f'\nPadres seleccionados: {[p for p in padres]}')
                self.logger.registrar_evento(f'\nHijos obtenidos: {[h for h in hijos]}\n')
            self.logger.registrar_evento(
                f'Evaluaciones realizadas hasta ahora: {self.num_evaluaciones} '
                f'| Mejor fitness actual: {min(ind.fitness for ind in self.poblacion):.2f}'
            )
            if self.generacion >= 1:
                self.logger.registrar_evento(f'\nGeneración {self.generacion}: Nuevos individuos generados:')
                for ixz, individuo in enumerate(hijos, start=1):
                    self.logger.registrar_evento(f"  Individuo: {ixz}  {individuo}")
            # --------------------------------LOGGING---------------------------------------#

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo
        self.logger.cerrar_log()


    def reemplazamiento(self, poblacion: list[Individuo]) -> list[Individuo]:
        """
        Devuelve nueva población formada por los n mejores de poblacion. Si se proporcionan elites entonces
        se garantiza que serán parte de la nueva población a través de un torneo de perdedores de k individuos
        """
        nueva_poblacion = sorted(poblacion, key=lambda i : i.fitness)[:len(self.poblacion)]
        if self.elites is not None:
            if self.p['kWorst'] < 0:
                ValueError("reemplazamiento_generacional(): k debe ser > 0 si elites != None")

            nuevos_individuos = set(nueva_poblacion)
            for elite in self.elites:
                if elite not in nuevos_individuos:
                    # Realizar el torneo para elegir un peor individuo
                    torneo = random.sample(range(len(nueva_poblacion)), self.p['kWorst'])
                    peor_individuo = max(torneo, key=lambda i: self.poblacion[i].fitness)

                    # Reemplazar al peor individuo por el individuo élite
                    nueva_poblacion[peor_individuo] = elite

        return nueva_poblacion

