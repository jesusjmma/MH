# Práctica 3 Metaheurísticas
Se ha llevado a cabo en Python3.

## Archivos
Para el correcto funcionamiento del programa debe estar presente el siguiente sistema de ficheros:
- datos_MDD → Es la carpeta que contiene todos los archivos con los datos del problema MDD
- Tablas_MDD_2021-22.xls → Es el archivo con las tablas modelo que se encuentra en PRADO
- executor.py → Es el programa principal que ejecuta los algoritmos
- es.py → Es el archivo que incluye el algorimo de Enfriamiento Simulado
- bmb.py → Es el archivo que incluye el algorimo de Búsqueda Multiarranque Básica
- ils.py → Es el archivo que incluye el algorimo de Búsqueda Local Reiterada
- ils_es.py → Es el archivo que incluye el algorimo de Hibridación de ILS y ES

## Ejecución
Para ejecutar el programa en su conjunto, se debe estar en la carpeta que contiene los archivos mencionados y ejecutar uno de los siguientes comandos:
- `python3 executor.py es`
- `python3 executor.py bmb`
- `python3 executor.py ils`
- `python3 executor.py ils_es`

El primero ejecutará el programa con la técnica de enfriamiento simulado, el segundo con la de búsqueda de multiarranque básica, el tercero con la de búsqueda local reiterada y el cuarto con la hibridación de ILS y ES.

También es posible ejecutar el algoritmo para un archivo concreto situado en la carpeta de datos_MDD. En este caso emplearemos el siguiente comando:
- `python3 algoritmo.py nombre_del_fichero semilla`

Donde `algoritmo.py` hace referencia a uno de los 4 archivos con el algoritmo a utilizar, `nombre_del_fichero` hace referencia al archivo situado en `datos_MDD` cuyos datos se desean emplear y `semilla` le indica a la librería random la inicialización.