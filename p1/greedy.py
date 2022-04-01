from random import randrange,choice,seed

def heur(n, remaining, myset, matrix, diff_sums):
    """Función greedy que construye la solución añadiendo el punto más favorable en cada momento.

        Parameters
        ----------
        n : int
            Cantidad de elementos totales que hay para elegir.
        remaining : set
            Elementos que aún están sin seleccionar.
        myset : set
            Elementos que ya están seleccionados
        matrix : list[list[int]]
            Distancias entre elementos.
        diff_sums : list[int]
            Dispersión entre los elementos seleccionados.

        Returns
        -------
        int
            Nuevo elemento a ser añadido a la solución.
        list[int]
            Suma de distancias de cada elemento añadido en la solución al resto de elementos añadidos en la solución.
        int
            Dispersión de los elementos añadidos en la solución.
        """
    sum=0
    d = [None] * n
    g = [None] * n

    for u in remaining:
        d[u] = diff_sums.copy()
        du = 0
        for v in myset:
            du += matrix[u][v]
            d[u][v] += matrix[u][v]

        dmax = max(du, max(filter(None, d[u])))
        dmin = min(du, min(filter(None, d[u])))

        d[u][u] = du

        g[u] =  dmax - dmin

    g2 = list(filter(None, g))
    if len(g2)==0:
        new_element = choice(list(remaining))
    else:
        new_element = g.index(min(list(filter(None, g))))

    return new_element, d[new_element], g[new_element]


def main(file, myseed):
    seed(myseed)

    file = open('datos_MDD/' + file)

    doc = file.readlines()

    n = int(doc[0].split()[0]) # Elementos totales
    m = int(doc[0].split()[1]) # Elementos a escoger

    matrix = [None] * n
    for i in range(n):
        matrix[i] = [None] * n

    for i in range(1,int(n*(n-1)/2)+1):
        line = doc[i].split()
        matrix[int(line[0])][int(line[1])] = float(line[2])
        matrix[int(line[1])][int(line[0])] = float(line[2])

    for i in range(0,n):
        matrix[i][i] = 0

    first_element = randrange(n)
    sol = {first_element}

    diff_sums = [None] * n
    diff_sums[first_element] = 0

    remaining = set(range(n))
    remaining.remove(first_element)

    while len(sol)<m:
        new_element, diff_sums, dispersion = heur(n, remaining, sol, matrix, diff_sums)
        sol.add(new_element)
        remaining.remove(new_element)
        print (diff_sums)

    return dispersion