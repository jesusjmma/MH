from random import seed,sample,choice,random
from math import ceil,exp
from sys import argv


def choose_sol(sol, remaining, sums, matrix):
    """Función que escoge un elemento a añadir y uno a quitar y nos devuelve una nueva solución con todo lo necesario

        Parameters
        ----------
        sol : set
            Elementos que están seleccionados en la propuesta de solución actual.
        remaining : set
            Elementos que NO están seleccionados en la propuesta de solución actual.
        sums : list[float]
            Suma de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.
        matrix : list[list[float]]
            Distancias entre elementos.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que NO están seleccionados en la nueva propuesta de solución.
        list[float]
            Suma de distancias de cada elemento añadido en la nueva solución al resto de elementos añadidos en la nueva solución.
    """
    new_sol = sol.copy()
    new_remaining = remaining.copy()
    new_sums = sums.copy()

    del_element = choice(list(sol))
    add_element = choice(list(remaining))

    new_sol.remove(del_element)
    new_sums[del_element] = None

    sum_add = 0

    for i in new_sol:
        new_sums[i] = new_sums[i] - matrix[del_element][i] + matrix[add_element][i]
        sum_add += matrix[add_element][i]
    new_sums[add_element] = sum_add

    new_sol.add(add_element)
    new_remaining.remove(add_element)
    new_remaining.add(del_element)

    maximum = float(max(i for i in new_sums if i is not None))
    minimum = float(min(i for i in new_sums if i is not None))

    return new_sol, new_remaining, new_sums, maximum-minimum


def main(file, myseed):
    """Función principal del programa que aplica el algoritmo ES.

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
    seed(myseed)

    file = open('datos_MDD/' + file)

    doc = file.readlines()

    n = int(doc[0].split()[0])  # Elementos totales
    m = int(doc[0].split()[1])  # Elementos a escoger

    matrix = [None] * n
    for i in range(n):
        matrix[i] = [0] * n

    for i in range(1, int(n * (n - 1) / 2) + 1):
        line = doc[i].split()
        matrix[int(line[0])][int(line[1])] = float(line[2])
        matrix[int(line[1])][int(line[0])] = float(line[2])

    sol = set(sample(range(n),m))
    sums = [None] * n
    remaining = set(range(n)) - sol

    for i in sol:
        sums[i] = 0
        for u in sol:
            sums[i] += matrix[i][u]
    maximum = float(max(i for i in sums if i is not None))
    minimum = float(min(i for i in sums if i is not None))

    cost = maximum-minimum
    T_0 = 0.249175063524761210746768 * cost # El coeficiente se ha obtenido al hacer mu = phi = 0.3, tal y como indica el guión de prácticas
    T_f = 0.001 # Este dato es el que se indica en el guión de prácticas

    if T_0 < T_f:
        return cost

    max_vecinos = 10*n
    max_exitos = n
    M = ceil(100000/max_vecinos)
    beta = (T_0-T_f)/(M*T_0*T_f)
    T_k = T_0

    best_sol = sol.copy()
    best_remaining = remaining.copy()
    best_sums = sums.copy()
    best_cost = cost

    while (T_f < T_k):
        vecinos=0
        exitos=0
        while (vecinos < max_vecinos and exitos < max_exitos):
            new_sol, new_remaining, new_sums, new_cost = choose_sol(sol, remaining, sums, matrix)
            cost_diff = new_cost - cost

            if (cost_diff<0 or random()<=exp(-cost_diff/T_k)):
                sol = new_sol
                remaining = new_remaining
                sums = new_sums
                cost = new_cost
                if(cost<best_cost):
                    best_sol = sol
                    best_remaining = remaining
                    best_sums = sums
                    best_cost = cost

                exitos += 1

            vecinos += 1

        T_k = T_k/(1+beta*T_k)

    print(best_sol)
    print(best_cost)
    return best_cost

if __name__ == "__main__":
    main(argv[1], argv[2])