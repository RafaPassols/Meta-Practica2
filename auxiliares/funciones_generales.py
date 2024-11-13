# auxiliares/funciones_generales.py

# Importaciones de bibliotecas estándar
import random

# Importaciones locales
# Importaciones de terceros


def generar_semillas(dni_alumno, num_semillas, offset=0) -> list[int]:
    """Genera una lista de semillas pseudoaleatorias"""
    if not isinstance(num_semillas, int) or num_semillas <= 0:
        raise ValueError("num_semillas debe ser entero mayor que 0.")

    random.seed(dni_alumno + offset)
    semillas = [random.randint(1, 100000) for _ in range(num_semillas)]

    return semillas


def factorizacion_2opt(tour, m, i, j) -> float:
    """
        Calcula la diferencia en distancia de un tour si se realizase un 2-opt en las posiciones (i,j)
        Parameters:
        - tour: permutación de ciudades
        - m: matriz de distancias
        . i,j: posiciones intercambiadas
    """
    n = len(tour)
    i, j = min(i, j), max(i, j)
    if j-i == 1 or (i == 0 and j == n-1):
        # Ciudades consecutivas
        arcos_desaparecen = m[tour[i - 1], tour[i]] + m[tour[j], tour[(j + 1) % n]]
        arcos_nuevos = m[tour[i - 1], tour[j]] + m[tour[i], tour[(j + 1) % n]]
    else:
        arcos_desaparecen = (
                m[tour[i - 1], tour[i]] + m[tour[i], tour[(i + 1) % n]] +
                m[tour[j - 1], tour[j]] + m[tour[j], tour[(j + 1) % n]]
        )
        arcos_nuevos = (
                m[tour[i - 1], tour[j]] + m[tour[j], tour[(i + 1) % n]] +
                m[tour[j - 1], tour[i]] + m[tour[i], tour[(j + 1) % n]]
        )

    return arcos_nuevos - arcos_desaparecen