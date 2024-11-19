# procesador_archivos.py

# Importaciones de bibliotecas estándar
import re

# Importaciones de terceros
import numpy as np
from scipy.spatial.distance import cdist


class ProcesadorTSP:
    """Procesa archivos de tipo .tsp para leer instancias de problemas específicos"""

    def __init__(self, archivo):
        self.archivo = archivo
        self.matriz_distancias = None
        self.tour = []
        self.identificadores = []


    def cargar_datos_tsp(self):
        """Devuelve la matriz de distancias"""
        try:
            with open(self.archivo, 'r') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f'Error: El archivo {self.archivo} no se encontró.')
            return None
        except Exception as e:
            print(f'Error al abrir el archivo {self.archivo}: {e}')
            return None

        coordenadas = []
        dimension = 0

        for i, linea in enumerate(lineas):
            if 'DIMENSION' in linea:
                dimension = int(linea.split(':')[1].strip())
                self.matriz_distancias = np.zeros((dimension, dimension))
            elif 'NODE_COORD_SECTION' in linea:
                for j in range(dimension):
                    ciudad, x, y = map(float, lineas[i + 1 + j].split())
                    coordenadas.append((x, y))
                    self.identificadores.append(int(ciudad))
            elif 'EOF' in linea:
                break

        # Calcula la matriz de distancias
        self.matriz_distancias = cdist(coordenadas, coordenadas, 'euclidean')
        return self.matriz_distancias


    def mostrar_tour(self, tour):
        # Convertir tour a lista si es una instancia de np.ndarray
        if isinstance(tour, np.ndarray):
            tour = tour.tolist()
        identificadores_tour = [self.identificadores[i] for i in tour]
        print("Tour:", identificadores_tour)


class ProcesadorTXT:
    """"Procesa archivos de tipo .txt para leer otros datos específicos"""

    def __init__(self, archivo):
        self.archivo = archivo
        self.parametros = {}


    def cargar_datos_txt(self):
        # Lógica para cargar y procesar el archivo .txt
        try:
            with open(self.archivo, 'r') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f'Error: El archivo {self.archivo} no se encontró.')
            return None
        except Exception as e:
            print(f'Error al abrir el archivo {self.archivo}: {e}')
            return None

        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('#') or not linea:
                continue

            match = re.match(r'(\w+)\s*=\s*(.+)', linea)
            if match:
                clave = match.group(1)
                valor = match.group(2).strip()

                # Para convertir aquellos parámetros que no sean cadenas en sus tipos correspondientes
                if valor.startswith('[') and valor.endswith(']'):
                    # Lista de cadenas
                    valor = [x.strip().strip("'\"") for x in valor[1:-1].split(',')]
                elif valor.isdigit():
                    valor = int(valor)
                elif valor.replace('.', '', 1).isdigit():
                    valor = float(valor)
                elif valor.lower() in ['yes', 'no']:
                    valor = valor.lower() == 'yes'

                # Almacena en el diccionario los parámetros leídos
                self.parametros[clave] = valor

        return self.parametros