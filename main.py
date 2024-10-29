import os
import sys

from utils.procesar_configuracion import Configuracion
from utils.procesar_tsp import TSP
from utils.utilidades import Utilidades


def main():
    if len(sys.argv) != 2:
        print("Uso: python ./main.py ./config.txt")
        sys.exit(1)

    # Procesar configuración
    archivo_configuracion = sys.argv[1]
    params = Configuracion(archivo_configuracion).procesar()

    print("Parámetros Procesados:")
    for clave, valor in params.items():
        print(f"{clave}: {valor}")

    # Generar las semillas a partir del DNI
    semillas = Utilidades.generar_semillas(params['dni'], params['num_ejecuciones'])

    print("Semillas generadas:", semillas)

    # Obtener la lista de archivos TSP desde la configuración
    archivos_tsp = params['archivos']

    # Crear logs solo si params['echo'] es False (antes era 'no')
    if not params['echo']:
        os.makedirs('logs', exist_ok=True)

    # Procesar cada archivo TSP
    for archivo_tsp in archivos_tsp:
        ruta_archivo = os.path.join('data', archivo_tsp)  # Construye la ruta completa
        tsp = TSP(ruta_archivo)  # Crea una instancia de TSP
        matriz_distancias= tsp.procesar()  # Procesa el archivo

        print(f"\n===========================")
        print(f"Procesado {archivo_tsp}:")
        print(f"===========================")



if __name__ == "__main__":
    main()