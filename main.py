# main.py

# Importaciones de bibliotecas estándar
import sys, os, random
import time
import multiprocessing as mp

# Importaciones locales
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
from auxiliares.crear_logs import Logger
from algoritmos.AlgGEN_Clase01_Grupo06 import Generacional
from algoritmos.AlgEST_Clase01_Grupo06 import Estacionario

# Importaciones de terceros
import numpy as np

def procesar_archivos_tsp(archivos_tsp, params, semillas) -> list[str]:
    resultados: list[str] = []
    for archivo in archivos_tsp:
        # Los archivos estarán guardados en una carpeta "data"
        ruta_archivo = os.path.join('data', archivo)
        if not os.path.exists(ruta_archivo):
            print(f'Error: El archivo {ruta_archivo} no se encontró.')
            continue

        print('========================')
        print(f'Procesando {archivo}:')
        print('========================')

        matriz = ProcesadorTSP(ruta_archivo).cargar_datos_tsp()
        for i, semilla in enumerate(semillas, start=1):
            random.seed(semilla)
            np.random.seed(semilla)
            processes = []
            queue = mp.Queue()
            log_gen = Logger(nombre_algoritmo='GEN', archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i,
                             echo=params['echo'])
            log_est = Logger(nombre_algoritmo='EST', archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i,
                             echo=params['echo'])

            if 'generacional' in params['algoritmos']:
                processes.append(mp.Process(target=ejecutar_generacional, args=(matriz, params, log_gen, queue)))
            if 'estacionario' in params['algoritmos']:
                processes.append(mp.Process(target=ejecutar_estacionario, args=(matriz, params, log_est, queue)))
            for p in processes:
                p.start()
            for p in processes:
                p.join()

            resultado = (
                f'--------------------------------------------------\n'
                f'Archivo: {archivo}    Semilla: {semilla}\n'
                f'--------------------------------------------------\n'
            )
            while not queue.empty():
                resultado += queue.get()
            resultados.append(resultado)
    print('\n')
    return resultados


def ejecutar_generacional(matriz, params, logger: Logger, queue: mp.Queue = None):
    generacional = Generacional(matriz, params, logger)
    generacional.ejecutar()
    result = (
        f'GENERACIONAL\n'
        f'Generación final alcanzada: {generacional.generacion}\n'
        f'Evaluaciones realizadas: {generacional.num_evaluaciones}\n'
        f'Tiempo de ejecucion: {generacional.tiempo_ejecucion}\n'
        f'Mejor individuo: {min(generacional.poblacion, key=lambda ind: ind.distancia)}\n\n'
        f''
    )
    del generacional
    if queue is not None:
        queue.put(result)
    return result


def ejecutar_estacionario(matriz, params, logger: Logger, queue: mp.Queue = None) -> str:
    estacionario = Estacionario(matriz, params, logger)
    estacionario.ejecutar()
    result = (
        f'ESTACIONARIO\n'
        f'Generación final alcanzada: {estacionario.generacion}\n'
        f'Evaluaciones realizadas: {estacionario.num_evaluaciones}\n'
        f'Tiempo de ejecucion: {estacionario.tiempo_ejecucion}\n'
        f'Mejor individuo: {min(estacionario.poblacion, key=lambda ind: ind.distancia)}\n\n'
    )
    del estacionario
    if queue is not None:
        queue.put(result)
    return result



def print_hi(name):
    """Muestra un mensaje de bienvenida."""
    print(f'👋 ¡Hola, {name}! Bienvenido al mundo de las soluciones optimizadas. 🚀🧬\n')


def procesar_config(archivo : str) -> dict:
    txt = ProcesadorTXT(archivo)
    return txt.cargar_datos_txt()


def generar_semillas(dni_alumno, num_semillas, offset=0) -> list[int]:
    """Genera una lista de semillas pseudoaleatorias"""
    if not isinstance(num_semillas, int) or num_semillas <= 0:
        raise ValueError("num_semillas debe ser entero mayor que 0.")

    random.seed(dni_alumno + offset)
    semillas = [random.randint(1, 100000) for _ in range(num_semillas)]

    return semillas



def main():
    """Función principal"""
    inicio = time.time()

    # Comprueba que se pasen dos argumentos
    if len(sys.argv) != 2:
        print('Uso: (python | py) ./main.py ./config.txt')
        sys.exit(1)

    params = procesar_config(sys.argv[1])
    print('Parámetros procesados:')
    for clave, valor in params.items():
        print(f'{clave}: {valor}')

    # Genera las semillas pseudoaleatorias
    semillas = generar_semillas(params['dni_alumno'], params['num_ejecuciones'])
    print(f'n.º de semillas: {params["num_ejecuciones"]}')
    print(f'semillas: {semillas}\n')

    # Procesa los archivos tsp
    archivos_tsp = params['archivos_tsp']
    results = procesar_archivos_tsp(archivos_tsp, params, semillas)
    for result in results:
        print(result)

    final = time.time()
    print(f'Tiempo de ejecución del programa: {final-inicio}')


if __name__ == '__main__':
    print_hi('Cristobal')
    main()