from random import seed,sample,choice,shuffle
from sys import argv


class Found(Exception):
    def __init__(self, e_del, e_add, sums, myset):
        self.e_del = e_del
        self.e_add = e_add
        self.sums = sums
        self.myset = myset


def heur(myset, remaining, matrix, sums, maximum, minimum):
    """Función que selecciona un elemento a quitar y uno a añadir a la solución actual para obtener un nuevo vecino.

        Parameters
        ----------
        myset : set
            Elementos que están seleccionados en la propuesta de solución actual.
        remaining : set
            Elementos que están sin seleccionar en la propuesta de solución actual.
        matrix : list[list[int]]
            Distancias entre elementos.
        sums : list[int]
            Suma de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.
        maximum : int
            Mayor de las sumas de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.
        minimum : int
            Menor de las sumas de las distancias de un nodo al resto de los que hay en la propuesta actual de solución.

        Returns
        -------
        int
            Nuevo elemento a ser añadido a la propuesta de solución actual.
        int
            Elemento a ser removido de la propuesta de solución actual.
        list[int]
            Suma de distancias de cada elemento añadido en la solución al resto de elementos añadidos en la solución.
        int
            Dispersión de los elementos añadidos en la solución.
    """

    average = (minimum+maximum)/2
    dist_sums = sums.copy()

    for i in range(len(myset)):
        if dist_sums[i] != None:
            dist_sums[i] = abs(dist_sums[i]-average)
    try:
        for i in range(len(myset)):
            e_del = dist_sums.index(choice([i for i in dist_sums if i is not None]))
            remaining_shuffled = [i for i in list(remaining) if i is not None]
            shuffle(remaining_shuffled)
            for e_add in remaining_shuffled:
                myset_prov = myset.copy()
                myset_prov.remove(e_del)
                sums_prov = sums.copy()
                sums_prov[e_del] = None
                sums_prov[e_add] = 0
                for e in myset_prov:
                    sums_prov[e] = sums_prov[e] - matrix[e_del][e] + matrix[e_add][e]
                    sums_prov[e_add] += matrix[e_add][e]
                myset_prov.add(e_add)
                if max(i for i in sums_prov if i is not None)-min(i for i in sums_prov if i is not None) < maximum-minimum:
                    raise Found(e_del, e_add, sums_prov, myset_prov)
            dist_sums[e_del] = None
    except Found as f:
        return f.e_add, f.e_del, f.sums
    else:
        return None, None, sums


def bl(sol, remaining, sums, cost, matrix, maximum, minimum):
    """Función de búsqueda local que construye la solución buscando el mejor vecino del actual en un máximo de iteraciones.

        Parameters
        ----------
        sol : set
            Elementos que están seleccionados en la nueva propuesta de solución.
        remaining : set
            Elementos que están sin seleccionar en la nueva propuesta de solución.
        sums : list[float]
            Suma de las distancias de un nodo al resto de los que hay en la nueva propuesta de solución.
        cost : float
            Coste de la nueva propuesta de solución.
        matrix : list[list[float]]
            Distancias entre elementos.
        maximum : float
            Elemento más grande en la lista sums.
        minimum : float
            Elemento más pequeño en la lista sums.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que están sin seleccionar en la nueva propuesta de solución.
        list[float]
            Suma de las distancias de un nodo al resto de los que hay en la nueva propuesta de solución.
        float
            Coste de la nueva propuesta de solución.
    """
    i = 0
    improvement = 1
    while i < 10000 and improvement > 0:
        new_element, removing_element, sums_NEW = heur(sol, remaining, matrix, sums, maximum, minimum)
        if new_element == None:
            return sol, remaining, sums, cost
        sol.remove(removing_element)
        sol.add(new_element)
        remaining.remove(new_element)
        remaining.add(removing_element)
        sums = sums_NEW.copy()
        maximum, minimum = max(i for i in sums if i is not None), min(i for i in sums if i is not None)
        improvement = cost - (maximum - minimum)
        cost = maximum - minimum

    return sol, remaining, sums, cost

def generate_sol(matrix,n,m):
    """Función que genera aleatoriamente una nueva solución.

        Parameters
        ----------
        matrix : list[list[float]]
            Distancias entre elementos.
        n : int
            Cantidad de elementos que hay en el problema.
        m : int
            Cantidad de elementos que se deben seleccionar para una solución del problema.

        Returns
        -------
        set
            Elementos que están seleccionados en la nueva propuesta de solución.
        set
            Elementos que están sin seleccionar en la nueva propuesta de solución.
        list[float]
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


def main(file, myseed):
    """Función principal del programa que aplica el algoritmo BMB.

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

    sol, remaining, sums, cost = generate_sol(matrix,n,m)

    best_sol = sol.copy()
    best_remaining = remaining.copy()
    best_sums = sums.copy()
    best_cost = cost

    for i in range(10):
        maximum, minimum = max(i for i in sums if i is not None), min(i for i in sums if i is not None)
        new_sol, new_remaining, new_sums, new_cost = bl(sol, remaining, sums, cost, matrix, maximum, minimum)

        if (new_cost < best_cost):
            best_sol = new_sol.copy()
            best_remaining = new_remaining.copy()
            best_sums = new_sums.copy()
            best_cost = new_cost
        
        sol, remaining, sums, cost = generate_sol(matrix,n,m)

    print(str(best_cost)+" - "+str(best_sol))
    return best_cost

if __name__ == "__main__":
    main(argv[1], argv[2])