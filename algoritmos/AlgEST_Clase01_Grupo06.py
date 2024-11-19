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
        return inicializar_poblacion(self.p['tamanio'], self.p['per_individuos'], self.p['k'], self.matriz_distancias)

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
            hijos = self.cruce(padres[0], padres[1])
            self.num_evaluaciones += 2

            for hijo in hijos:
                if random.random() < self.p['per_mutacion']:
                    hijo.intercambio_2opt()
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
                f'| Mejor fitness actual: {min(ind.distancia for ind in self.poblacion):.2f}'
            )
            # --------------------------------LOGGING---------------------------------------#

        self.tiempo_ejecucion = time.time() - self.inicio_tiempo
        self.logger.cerrar_log()

    def reemplazamiento(self, hijo1: Individuo, hijo2: Individuo):
        """Elimina dos indiviuos de la población y coloca a los hijos"""
        for hijo in [hijo1, hijo2]:
            torneo = random.sample(range(len(self.poblacion)), self.p['kWorst'])
            peor_individuo = max(torneo, key=lambda i: self.poblacion[i].distancia)
            self.poblacion[peor_individuo] = hijo