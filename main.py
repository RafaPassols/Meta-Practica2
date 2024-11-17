# main.py

# Importaciones de bibliotecas estándar
import sys, os, random

# Importaciones locales
from auxiliares.crear_logs import Logger
from auxiliares.funciones_generales import generar_semillas
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
from algoritmos.AlgGEN_Clase01_Grupo06 import Generacional
from algoritmos.AlgEST_Clase01_Grupo06 import Estacionario

# Importaciones de terceros
import numpy as np


def procesar_archivos_tsp(archivos_tsp, params, semillas):
    """Procesamiento de los archivos (.tsp)."""

    # Lista para almacenar los resultados
    resultados: list[str] = []

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

            # Crea los ficheros logs
            log_gen = Logger(nombre_algoritmo='GEN', archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i, echo=params['echo'])
            log_est = Logger(nombre_algoritmo='EST', archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i, echo=params['echo'])

            resultados.append(
                f'--------------------------------------------------\n'
                f'Archivo: {archivo}    Semilla: {semilla}\n'
                f'--------------------------------------------------\n'
            )

            # Ejecuta el algoritmo evolutivo generacional
            if 'generacional' in params['algoritmos']:
                generacional = Generacional(matriz, params, log_gen)  # Crea una instancia del algoritmo generacional
                generacional.ejecutar()  # Ejecuta el algoritmo

                # Muestra resultados
                resultados.append(
                    f'GENERACIONAL\n'
                    f'Generación final alcanzada: {generacional.generacion}\n'
                    f'Evaluaciones realizadas: {generacional.evaluaciones}\n'
                    f'Mejor individuo: {min(generacional.poblacion, key=lambda ind: ind.fitness)}\n'
                )

            # Ejecuta el algoritmo evolutivo estacionario
            if 'estacionario' in params['algoritmos']:
                estacionario = Estacionario(matriz, params, log_est)  # Crea una instancia del algoritmo estacionario
                estacionario.ejecutar()  # Ejecuta el algoritmo

                # Muestra resultados
                resultados.append(
                    f'ESTACIONARIO\n'
                    f'Generación final alcanzada: {estacionario.generacion}\n'
                    f'Evaluaciones realizadas: {estacionario.evaluaciones}\n'
                    f'Mejor individuo: {min(estacionario.poblacion, key=lambda ind: ind.fitness)}\n'
                )

        print('\n')

    return resultados



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
    resultados = procesar_archivos_tsp(archivos_tsp, params, semillas)

    for resultado in resultados:
        print(resultado)


if __name__ == '__main__':
    main()