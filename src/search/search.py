import signal
import numpy as np

from ec import EC


def start(input_file, output_file, max_time):
    A = read_input(input_file)

    ec = EC(A, max_time)
    signal.signal(signal.SIGINT, ec.stop)

    COV, execution_time = ec.start()

    write_output(output_file, A, COV, execution_time)

    print(f'Tempo impiegato: {execution_time}\n')
    print(f'File di output \"{output_file}\" creato\n')


def read_input(input_file):
    A = []

    with open(input_file, "r") as file:
        for line in file:
            if ';;;' in line:
                continue
            if '-' in line:
                line = list(line.split())
                elements = []
                for element in line[0:-1]:
                    elements.append(int(element))
                A.append(elements)

    return np.array(A, dtype=int)


def write_output(output_file, A, COV, execution_time):
    with open(output_file, "w") as file:
        idx = 1
        for x in A:
            file.write(f';;; Insieme {str(idx)}\n{str(x)}\n')
            idx += 1
        file.write('\n;;; COV:\n')
        if COV == []:
            file.write(';;; Copertura esatta NON trovata\n')
        else:
            for x in COV:
                x = np.array(x, dtype=int)
                file.write(str(x+1) + '\n')
        file.write('\n;;; Algoritmo EC\n')
        file.write(';;; Tempo di esecuzione: ' + str(execution_time) +
                   ' s (' + str(round(execution_time/60, 3)) + ' minutes) \n')
