# algoritmos/AlgGEN_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.individuo import Individuo
from auxiliares.funciones_generales import funcion_objetivo, cruce_ox2, cruce_moc
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio

# Importaciones de tercero
import numpy as np


class Generacional:
    """Implementa el algoritmo evolutivo generacional (GEN)."""

    def __init__(self, matriz, params, logger=None):
        self.matriz = matriz
        self.params = params
        self.generacion = None
        self.poblacion = []             # Lista de individuos (soluciones)
        self.evaluaciones = 0           # Evaluaciones realizadas
        self.elite = []                 # Almacena el individuo élite (depende de 'E')
        self.inicio_tiempo = time.time()
        self.tiempo_ejecucion = None
        self.logger = logger            # Logger para registrar eventos


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo generacional."""

        self.logger.registrar_evento('Iniciando ejecución del algoritmo generacional.')

        self.generacion = 0
        self.inicializar_poblacion()
        self.evaluar(self.poblacion)

        self.logger.registrar_evento('Población inicial generada:')
        for idx, individuo in enumerate(self.poblacion, start=1):
            self.logger.registrar_evento(f'  Individuo: {idx}  {individuo}')

        while (self.evaluaciones < self.params['max_evaluaciones']) and (time.time() - self.inicio_tiempo < self.params['tiempo']):

            # t = t+1
            self.generacion += 1

            if self.generacion == 1:
                self.logger.registrar_evento('=== Inicio de la Generación 0 ===')

            # Guardamos los mejores individuos (elitismo) de P(t) para no perderlos
            self.elite = sorted(self.poblacion, key=lambda ind: ind.fitness)[:self.params['E']]
            self.logger.registrar_evento(f'Elite de la generación {self.generacion - 1}: {[e for e in self.elite]}')

            # Selecciona la población intermedia P´ desde P(t-1)
            poblacion_padres = self.seleccionar()
            if self.generacion == 1:
                self.logger.registrar_evento(f'\nPoblación de padres seleccionada: {[p for p in poblacion_padres]}')

            # Recombina los individuos de la población P´para obtener la descendencia
            nueva_poblacion = self.recombinar(poblacion_padres)
            if self.generacion == 1:
                self.logger.registrar_evento(f'\nDescendencia generada: {[n for n in nueva_poblacion]}\n')

            # Muta los individuos de la población
            self.mutar(nueva_poblacion)
            if self.generacion == 1:
                self.logger.registrar_evento(f'Mutaciones aplicadas a la descendencia.')

            # Evalúa la nueva población de individuos generada P(t)
            self.evaluar(nueva_poblacion)
            self.logger.registrar_evento(f'Evaluando nueva población descendiente...')
            self.logger.registrar_evento(f'Evaluaciones realizadas hasta ahora: {self.evaluaciones} | Mejor fitness actual: {min(ind.fitness for ind in nueva_poblacion):.2f}')

            # Reemplaza la población actual por la nueva
            self.reemplazar(nueva_poblacion)
            if self.generacion >= 1:
                self.logger.registrar_evento(f'\nGeneración {self.generacion}: Nuevos individuos generados:')
                for ixz, individuo in enumerate(nueva_poblacion, start=1):
                    self.logger.registrar_evento(f"  Individuo: {ixz}  {individuo}")

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
                individuo.generacion = self.generacion
                self.evaluaciones += 1


    def seleccionar(self):
        """Operador de selección basado en un torneo binario con kBest."""

        poblacion_padres = []

        for _ in range(len(self.poblacion)):

            # Selecciona kBest individuos del torneo
            while True:
                torneo = random.sample(self.poblacion, self.params['kBest'])
                # Nos aseguramos que ambos individuos sean distintos
                if len(torneo) == len(set(torneo)):
                    break

            # Selecciona al mejor individuo del torneo
            mejor = min(torneo, key=lambda ind: ind.fitness)
            poblacion_padres.append(mejor)

        # Log para la primera generación
        if self.generacion == 1:
            self.logger.registrar_evento(f'Torneo: {[ind for ind in torneo]} -> Seleccionado: {mejor}')

        return poblacion_padres


    def recombinar(self, poblacion_padres):
        """Recombina con una cierta probabilidad los individuos de la población."""

        poblacion_hijos = []
        cruce = self.params['cruce']
        num_lanzamientos = int(len(poblacion_padres) / 2)

        for _ in range(num_lanzamientos):

            # Selecciona dos padres aleatoriamente
            padre_1, padre_2 = random.sample(poblacion_padres, 2)

            # Lanzamiento aleatorio (moneda)
            if random.random() < self.params['per_cruce']:

                if cruce == 'OX2':
                    hijo_1, hijo_2 = cruce_ox2(padre_1, padre_2)
                else:
                    hijo_1, hijo_2 = cruce_moc(padre_1, padre_2)

                # Establezco la generación en que fueron generados
                hijo_1.generacion = self.generacion
                hijo_2.generacion = self.generacion
            else:
                # No cruza los padres y los mantiene en la población descendiente (no actualiza la generación)
                hijo_1, hijo_2 = padre_1, padre_2

            poblacion_hijos.extend([hijo_1, hijo_2])

        # Log para la primera generación
        if self.generacion == 1:
            self.logger.registrar_evento(
                f'Cruce: P1 {padre_1}, P2 {padre_2} -> '
                f'H1 {hijo_1 if hijo_1.flag else 'Sin evaluar'}, '
                f'H2 {hijo_2 if hijo_2.flag else 'Sin evaluar'}'
            )

        return poblacion_hijos


    def mutar(self, nueva_poblacion):
        """Aplica la mutación con una cierta probabilidad a cada individuo de la población."""

        for individuo in nueva_poblacion:
            if random.random() < self.params['per_mutacion']:
                # Muta al individuo (aplica 2-opt)
                individuo.intercambio_2_opt(self.matriz)

                # Log para primera generación
                if self.generacion == 1:
                    self.logger.registrar_evento(f'Mutación aplicada a individuo: {individuo}')


    def reemplazar(self, nueva_poblacion):
        """Reemplaza por completo la población de individuos preservando el elitismo."""

        # Creamos un conjunto con las distancias del elitismo
        conjunto_elite = set(self.elite)

        # Creamos un conjunto con los fitness de la nueva población
        fitness_nueva_poblacion = {ind.fitness for ind in nueva_poblacion}

        for elite in conjunto_elite:
            if elite.fitness not in fitness_nueva_poblacion:

                # Realiza un torneo de perdedores
                while True:
                    torneo = random.sample(nueva_poblacion, self.params['kWorst'])
                    # Nos aseguramos que ambos individuos sean distintos
                    if len(torneo) == len(set(torneo)):
                        break

                peor = max(torneo, key=lambda ind: ind.fitness)
                nueva_poblacion.remove(peor)
                nueva_poblacion.append(elite)

                # Log para primera generación
                if self.generacion == 1:
                    self.logger.registrar_evento(f'Reemplazo: Peor individuo {peor} sustituido por élite {elite}')

        # Reemplaza por completo a la población
        self.poblacion = nueva_poblacion