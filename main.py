import sys

from utils.procesar_configuracion import Configuracion


def main():
    if len(sys.argv) != 2:
        print("Uso: python ./main.py ./config.txt")
        sys.exit(1)

    # Procesar configuración
    archivo_configuracion = sys.argv[1]
    params = Configuracion(archivo_configuracion).procesar()

    for key in params:
        print(f'{key} -> {params[key]}')

if __name__ == "__main__":
    main()