from random import seed, sample, choice, shuffle, random
from math import ceil, exp
from sys import argv


class Found(Exception):
    def __init__(self, e_del, e_add, sums, myset):
        self.e_del = e_del
        self.e_add = e_add
        self.sums = sums
        self.myset = myset


def choose_sol(sol, remaining, sums, matrix):
    """Función que escoge un elemento a añadir y uno a quitar y nos devuelve una nueva solución con todo lo necesario

        Parameters
        ----------
        sol : set
            Elementos que están seleccionados en la propuesta de solución actual.
        remaining : set
            Elementos que NO están seleccionados en la propuesta de solución actual.
        sums : list[int]
            Suma de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.
        matrix : list[list[int]]
            Distancias entre elementos.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que NO están seleccionados en la nueva propuesta de solución.
        list[int]
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


def es(sol, remaining, sums, cost, matrix):
    T_0 = 0.249175063524761210746768 * cost
    T_f = 0.001

    if T_0 < T_f:
        return sol, remaining, sums, cost

    n = len(matrix[0])
    max_vecinos = 10 * n
    max_exitos = n
    M = ceil(10000 / max_vecinos)
    beta = (T_0 - T_f) / (M * T_0 * T_f)
    T_k = T_0

    best_sol = sol.copy()
    best_remaining = remaining.copy()
    best_sums = sums.copy()
    best_cost = cost

    while (T_f < T_k):
        vecinos = 0
        exitos = 0
        while (vecinos < max_vecinos and exitos < max_exitos):
            new_sol, new_remaining, new_sums, new_cost = choose_sol(sol, remaining, sums, matrix)
            cost_diff = new_cost - cost

            if (cost_diff < 0 or random() <= exp(-cost_diff / T_k)):
                sol = new_sol
                remaining = new_remaining
                sums = new_sums
                cost = new_cost
                if (cost < best_cost):
                    best_sol = sol
                    best_remaining = remaining
                    best_sums = sums
                    best_cost = cost

                exitos += 1

            vecinos += 1

        T_k = T_k / (1 + beta * T_k)

    return sol, remaining, sums, cost


def generate_sol(matrix, n, m):
    """Función de búsqueda local que construye la solución buscando un vecino mejor al actual.

        Parameters
        ----------
        matrix : list[list[int]]
            Distancias entre elementos.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que están sin seleccionar en la nueva propuesta de solución.
        list[int]
            Suma de las distancias de un nodo al resto de los que hay en la nueva propuesta de solución.
        float
            Coste de la nueva propuesta de solución.
    """
    sol = set(sample(range(n), m))
    sums = [None] * n
    remaining = set(range(n)) - sol

    for i in sol:
        sums[i] = 0
        for u in sol:
            sums[i] += matrix[i][u]
    maximum = float(max(i for i in sums if i is not None))
    minimum = float(min(i for i in sums if i is not None))

    cost = maximum - minimum

    return sol, remaining, sums, cost


def mutation(sol, remaining, sums, matrix):
    """Función que escoge varios elemento a añadir y varios a quitar y nos devuelve una nueva solución con todo lo necesario

        Parameters
        ----------
        sol : set
            Elementos que están seleccionados en la propuesta de solución actual.
        remaining : set
            Elementos que NO están seleccionados en la propuesta de solución actual.
        sums : list[int]
            Suma de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.
        matrix : list[list[int]]
            Distancias entre elementos.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que NO están seleccionados en la nueva propuesta de solución.
        list[int]
            Suma de distancias de cada elemento añadido en la nueva solución al resto de elementos añadidos en la nueva solución.
    """
    new_sol = sol.copy()
    new_remaining = remaining.copy()
    new_sums = sums.copy()

    shuffled_sol = list(new_sol)
    shuffle(shuffled_sol)
    shuffled_remaining = list(new_remaining)
    shuffle(shuffled_remaining)

    num_change = ceil(0.3*len(sol))
    del_elements = set(shuffled_sol[0:num_change])
    add_elements = set(shuffled_remaining[0:num_change])

    new_sol = new_sol-del_elements
    for i in del_elements:
        new_sums[i] = None

    n = len(matrix[0])
    sum_add = [0] * n


    for i in new_sol:
        for j in del_elements:
            new_sums[i] = new_sums[i] - matrix[j][i]
        for j in add_elements:
            sum_add[j] = sum_add[j] + matrix[j][i]

    for i in add_elements:
        for j in add_elements:
            sum_add[j] = sum_add[j] + matrix[j][i]

    for i in range(n):
        if (sum_add[i]>0):
            new_sums[i] = sum_add[i]

    new_sol = new_sol.union(add_elements)
    new_remaining = new_remaining-add_elements
    new_remaining = new_remaining.union(del_elements)

    maximum = float(max(i for i in new_sums if i is not None))
    minimum = float(min(i for i in new_sums if i is not None))

    return new_sol, new_remaining, new_sums, maximum-minimum


def main(file, myseed):
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

    sol, remaining, sums, cost = generate_sol(matrix, n, m)
    sol, remaining, sums, cost = es(sol, remaining, sums, cost, matrix)

    best_sol = sol.copy()
    best_remaining = remaining.copy()
    best_sums = sums.copy()
    best_cost = cost

    for i in range(9):
        sol, remaining, sums, cost = mutation(best_sol, best_remaining, best_sums, matrix)
        sol, remaining, sums, cost = es(sol, remaining, sums, cost, matrix)

        if (cost < best_cost):
            best_sol = sol.copy()
            best_remaining = remaining.copy()
            best_sums = sums.copy()
            best_cost = cost

        sol, remaining, sums, cost = generate_sol(matrix, n, m)

    print(str(best_cost) + " - " + str(best_sol))
    return best_cost


if __name__ == "__main__":
    main(argv[1], argv[2])