import random
import Alg01_Clase01_Grupo06
from algoritmos.Alg01_Clase01_Grupo06 import GreedyAleatorio


class Solucion:
    # Camino que recorre todas las ciudades
    tour = []
    # Distancia del tour
    distancia = 0
    # Flag para guardar si la distancia está actualizada
    updated = False

    def __init__(self, tour, distancia, updated):
        self.tour = tour
        self.distancia = distancia
        self.updated = updated

class Generacional:
    # PARÁMETROS POBLACIÓN INICIAL
    # Tamaño población inicial
    tam_poblacion_inicial = 0
    sol = Solucion([1,2,3], 1, True)
    # % de la población generada con greedy aleatorio
    factor_greedy = 0.0

    # % de la población generada aleatoriamente
    factor_aleatorio = 0.0

    # MUTACIÓN Y CRUCE
    # Operador para recombinar soluciones (ox2 / moc)
    cruce = None

    # Operador para mutar
    mutacion = None

    # Probabilidad de que los individuos seleccionados se crucen
    factor_cruce = 0.0

    # Probabilidad de mutación
    factor_mutacion = 0.0

    # SELECCION
    # Cuántos élites guardamos
    num_elites = 0

    # Parámetro del torneo de ganadores
    k_mejores = 0

    # Parámetro del torneo de los peores en el reemplazamiento
    k_peores = 0

    poblacion = []
    greedy = None
    semilla = 0

    def __init__(self, matriz_distancias, params, semilla):
        self.tam_poblacion_inicial = params['tam_poblacion_inicial']
        self.factor_greedy = params['factor_greedy']
        self.factor_aleatorio = params['factor_aleatorio']

        if params['cruce'] is 'OX2':
            self.fcruce = ox2()
        elif params['cruce'] is 'MOC':
            self.cruce = moc()
        self.mutacion = intercambio_2opt()
        self.factor_cruce = params['factor_cruce']
        self.factor_mutacion = params['factor_mutacion']

        self.num_elites = params['num_elites']
        self.k_mejores = params['k_mejores']
        self.k_peores = params['k_peores']

        self.semilla = semilla
        self.greedy = GreedyAleatorio(matriz_distancias, params, self.semilla)
        self.inicializar_poblacion()


    def inicializar_poblacion(self):
        tam_aleatorio = int(self.tam_poblacion_inicial*self.factor_aleatorio)
        tam_greedy = self.tam_poblacion_inicial - tam_aleatorio



def ox2 (solA: list[int], solB: list[int]) -> list[int]:
    pass

def moc (solA: list[int], solB: list[int]) -> list[int]:
    pass

# Intercambia dos posiciones aleatoriamente
def intercambio_2opt (sol : list[int]) -> list[int]:
    i = random.randint(0, len(sol)-1)
    j = random.randint(0, len(sol)-1)
    sol[i], sol[j] = sol[j], sol[i]
    return sol
