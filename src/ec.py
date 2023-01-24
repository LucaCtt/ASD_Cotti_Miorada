from datetime import datetime
import numpy as np
import time


class EC:
    def __init__(self, A, time_limit):
        self.__A = A
        self.__time_limit = time_limit

        self.__n, self.__m = A.shape
        self.__COV = []
        self.__B = np.zeros((self.__n, self.__n), dtype=int)

        # Array di 0 per controllare se A[i] è vuota
        self.__zeros = np.zeros(self.__m, dtype=int)

        # Array di 1 per controllare se A[i] è uguale a M
        self.__ones = np.ones(self.__m, dtype=int)

        # Flag che indica se la ricerca deve essere interrotta
        self.__stop_flag = False

        self.__start_time = time.time()
        self.__visited_count = 0

    def start(self):
        for i in range(0, self.__n):
            if self.__should_stop():
                break

            self.__visited_count += 1

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

                self.__visited_count += 1

                if np.bitwise_and(self.__A[j], self.__A[i]).any():
                    self.__B[j, i] = 0
                else:
                    I = np.array([i, j])
                    U = np.bitwise_or(self.__A[i], self.__A[j])
                    if np.array_equal(U, self.__ones):
                        self.__COV.append(I)
                        self.__B[j, i] = 0
                    else:
                        self.__B[j, i] = 1
                        Inter = np.bitwise_and(
                            self.__B[0:j, i], self.__B[0:j, j])
                        if Inter.size > 0 and not np.array_equal(Inter, np.zeros(len(Inter), dtype=int)):
                            self.__esplora(I, U, Inter)

        execution_time = time.time() - self.__start_time
        return self.__COV, self.__visited_count, execution_time

    def stop(self):
        self.__should_stop = True

    def __esplora(self, I, U, Inter):
        for k in range(0, len(Inter)):
            if self.__should_stop():
                break

            if Inter[k] == 1:
                Itemp = np.append(I.copy(), k)
                Utemp = np.bitwise_or(U, self.__A[k])

                if np.array_equal(Utemp, self.__ones):
                    self.__COV.append(Itemp)
                else:
                    Intertemp = np.bitwise_and(Inter[0:k], self.__B[0:k, k])
                    if Intertemp.size > 0 and not np.array_equal(Intertemp, np.zeros(len(Intertemp), dtype=int)):
                        self.__esplora(Itemp, Utemp, Intertemp)

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


def write_output(output_file, A, COV, visited_count, execution_time):
    with open(output_file, "w") as file:
        file.write(';;; EC Algorithm \n')
        file.write(f';;; Executed at: {datetime.today()}\n')
        file.write(
            f';;; Execution time: {execution_time}s ({round(execution_time/60, 3)} minutes) \n')
        file.write(f';;; Nodes visited: {visited_count}\n\n')

        idx = 1
        for x in A:
            file.write(f';;; Set {idx}:\n{x}\n')
            idx += 1

        file.write('\n;;; Exact Coverages:\n')
        if COV == []:
            file.write(';;; No coverage found.\n')
        else:
            for x in COV:
                x = np.array(x, dtype=int)
                file.write(f'{x+1}\n')
