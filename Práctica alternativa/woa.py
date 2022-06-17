from random import seed, sample, choice, shuffle, random
from math import exp
from sys import argv


def woa(n):

    Inicializa aleatoriamente cada Xi (i= 1,2, …, n)
    Calcula el fitness de cada Xi
    X’= mejor(Xi)
    while (t < maximo_iteraciones), hacer:
        for (each Xi), hacer:
            Actualizar a, A, C, l, p
            if (p < 0.5), hacer:
                if (|A| < 1), hacer:
                    Actualiza la posición del Xi actual siguiendo (1)
                    else, hacer:  #Esto ocurre cuando |A| ≥ 1
                        Selecciona un agente de búsqueda aleatorio (Xaleatorio)
                        Actualiza la posición del agente de búsqueda Xi siguiendo (5)
                end if
                else, hacer:  #Esto ocurre cuando p ≥ 0.5
                    Actualiza la posición del agente de búsqueda Xi actual siguiendo (4)
            end if
        end for
        Comprueba si algún agente ha sobrepasado el espacio de búsqueda y arreglarlo
        Calcula el fitness de cada agente de búsqueda Xi
        Actualizar X’ si hay una solución mejor
        t = t + 1
    end while
    return X’


def main(file, myseed):
    """Función principal del programa que aplica el algoritmo WOA al problema MDD.

        Parameters
        ----------
        file : string
            Nombre del archivo del que obtener los datos.
        myseed : int o string
            Semilla para la librería random.

        Returns
        -------
        float
            Coste de la solución.
    """






if __name__ == "__main__":
    main(argv[1], argv[2])