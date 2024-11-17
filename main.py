# main.py

# Importaciones de bibliotecas estándar
import sys, os, random

# Importaciones locales
from auxiliares.funciones_generales import generar_semillas
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
from algoritmos.AlgGEN_Clase01_Grupo06 import Generacional
from algoritmos.AlgEST_Clase01_Grupo06 import Estacionario

# Importaciones de terceros
import numpy as np


def procesar_archivos_tsp(archivos_tsp, params, semillas):
    """Procesamiento de los archivos (.tsp)."""

    for archivo in archivos_tsp:
        ruta_archivo = os.path.join('data', archivo)

        if not os.path.exists(ruta_archivo):
            print(f'Error: El archivo {ruta_archivo} no se encontró.')
            continue

        tsp = ProcesadorTSP(ruta_archivo)
        matriz, tour = tsp.cargar_datos_tsp()

        print('\n========================')
        print(f'Procesando {archivo}:')
        print('========================')

        for i, semilla in enumerate(semillas, start=1):
            random.seed(semilla)
            np.random.seed(semilla)

            # PRUEBA 03: Generacional
            # Ejecuta el algoritmo evolutivo generacional
            if 'generacional' in params['algoritmos']:
                print(f'Ejecutando Algoritmo GENERACIONAL con la semilla {semilla}:')
                generacional = Generacional(matriz, params)  # Crea una instancia del algoritmo generacional
                generacional.ejecutar()  # Ejecuta el algoritmo

                # Muestra resultados
                print(f'Generación final alcanzada: {generacional.generacion}')
                print(f'Evaluaciones realizadas: {generacional.evaluaciones}')
                mejor_individuo = min(generacional.poblacion, key=lambda ind: ind.fitness)
                print(f'Mejor tour encontrado: {mejor_individuo.tour}')
                print(f'Distancia total del mejor tour: {mejor_individuo.fitness:.2f}\n')

            # PRUEBA 04: Estacionario
            # Ejecuta el algoritmo evolutivo estacionario
            if 'estacionario' in params['algoritmos']:
                print(f'Ejecutando Algoritmo ESTACIONARIO con la semilla {semilla}:')
                estacionario = Estacionario(matriz, params)  # Crea una instancia del algoritmo estacionario
                estacionario.ejecutar()  # Ejecuta el algoritmo

                # Muestra resultados
                print(f'Generación final alcanzada: {estacionario.generacion}')
                print(f'Evaluaciones realizadas: {estacionario.evaluaciones}')
                mejor_individuo = min(estacionario.poblacion, key=lambda ind: ind.fitness)
                print(f'Mejor tour encontrado: {mejor_individuo.tour}')
                print(f'Distancia total del mejor tour: {mejor_individuo.fitness:.2f}\n')



def main():
    """Función principal"""

    # Comprueba que se pasen dos argumentos
    if len(sys.argv) != 2:
        print('Uso: (python | py) ./main.py ./config.txt')
        sys.exit(1)

    # Carga los datos del config.txt
    archivo_config = sys.argv[1]
    txt = ProcesadorTXT(archivo_config)
    params = txt.cargar_datos_txt()

    print('Parámetros procesados:')
    for clave, valor in params.items():
        print(f'{clave}: {valor}')

    # Genera las semillas pseudoaleatorias
    semillas = generar_semillas(params['dni_alumno'], params['num_ejecuciones'])

    print(f'n.º de semillas: {params["num_ejecuciones"]}')
    print('semillas:', semillas)

    # Carga los archivos .tsp
    archivos_tsp = params['archivos_tsp']

    # Crear logs si params['echo'] es False
    if not params['echo']:
        os.makedirs('logs', exist_ok=True)

    # Procesa los archivos
    procesar_archivos_tsp(archivos_tsp, params, semillas)


if __name__ == '__main__':
    main()