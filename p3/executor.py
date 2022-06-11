from os import listdir
from pandas import read_excel, DataFrame, concat
from time import process_time_ns
from sys import argv
import es


def main(algorithm):
    total_time_start = process_time_ns()

    perfect_timing = {}
    timing={}
    medias={}
    times={}

    table = read_excel('Tablas_MDD_2021-22.xls')
    table.to_dict()

    for i in range(2,52):
        perfect_timing[table['Nº casos:'][i]] = table['Unnamed: 3'][i]

    for file in listdir('datos_MDD'):
        disp = [None]*5
        desv = 0
        media = 0
        time_start={}
        time_end={}
        time=[]
        for i in range(5):
            time_start[i] = process_time_ns()
            disp = es.main(file,i) if algorithm == 'es' else return 1
            time_end[i] = process_time_ns()
            time.append(time_end[i]-time_start[i])
            if disp != 0:
                desv += (disp - perfect_timing[file[:-4]]) / disp
            media += disp
        times[file[:-4]] = sum(time)/5
        media = media / 5
        timing[file[:-4]] = 100*desv
        medias[file[:-4]] = media

    total_time_end = process_time_ns()
    total_time = total_time_end - total_time_start

    df_desv = DataFrame.from_dict(timing, orient='index')
    df_desv = df_desv.rename(columns={0: 'Desviacion'})
    df_best = DataFrame.from_dict(perfect_timing, orient='index')
    df_best = df_best.rename(columns={0: 'Mejor coste'})
    df_cost = DataFrame.from_dict(medias, orient='index')
    df_cost = df_cost.rename(columns={0: 'Coste medio'})
    df_time = DataFrame.from_dict(times, orient='index')
    df_time = df_time.rename(columns={0: 'Tiempo medio (ns)'})

    df = concat([df_best, df_cost, df_desv, df_time], axis=1)

    print(df)
    df.to_excel('timing.xlsx', sheet_name=algorithm)
    print(str(total_time/1000000000) + ' segs.')

if __name__ == "__main__":
    main(argv[1])