import numpy as np
import time


class EC:
    def __init__(self, A, time_limit):
        self.__A = A
        self.__rows, self.cols = A.shape
        self.__COV = []
        self.__B = np.zeros((self.__rows, self.__rows), dtype=int)

        # Array di 0 per controllare se A[i] è vuota
        self.__zeros = np.zeros(self.cols, dtype=int)

        # Array di 0 per controllare se A[i] è uguale a M
        self.__ones = np.ones(self.cols, dtype=int)

        # Flag che indica se la ricerca deve essere interrotta
        self.__stop_flag = False

        self.__start_time = time.time()
        self.__time_limit = time_limit

    def start(self):
        for i in range(0, self.__rows):
            if self.__should_stop():
                break

            if (self.__A[i] == self.__zeros).all():
                continue
            # Controllare che A[i] sia uguale a M
            # coincide con il controllare che contenga tutti 1
            elif (self.__A[i] == self.__ones).all():
                self.__COV.append([i])
                continue

            for j in range(0, i):
                if self.__should_stop():
                    break

                if np.intersect1d(self.__A[j], self.__A[i]).any():
                    self.__B[j, i] = 0
                else:
                    I = np.array([i, j])
                    U = np.union1d(self.__A[i], self.__A[j])
                    if (U == self.__ones).all():
                        self.__COV.append(I)
                        self.__B[j, i] = 0
                    else:
                        self.__B[j, i] = 1
                        Inter = np.intersect1d(
                            self.__B[0:j, i], self.__B[0:j, j])
                        if len(Inter) > 0 and (Inter != np.zeros(len(Inter), dtype=int)).any():
                            self.__esplora(I, U, Inter)

        execution_time = time.time() - self.__start_time
        return self.__COV, execution_time

    def stop(self):
        self.__should_stop = True

    def __esplora(self, I, U, Inter):
        for k in range(0, len(Inter)):
            if self.__should_stop():
                break

            if Inter[k] == 1:
                Itemp = np.append(I.copy(), k)
                Utemp = np.union1d(U, self.__A[k])

                if (Utemp == self.__ones).all():
                    self.__COV.append(Itemp)
                else:
                    Intertemp = np.intersect1d(Inter[0:k], self.__B[0:k, k])
                    if len(Intertemp) > 0 and (Intertemp != np.zeros(len(Intertemp), dtype=int)).any():
                        self.esplora(Itemp, Utemp, Intertemp)

    def __should_stop(self):
        if self.__stop_flag:
            return True

        if self.__time_limit is None:
            return False

        return (time.time() - self.__start_time > self.__time_limit)


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
