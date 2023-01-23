import numpy as np
import time


class EC():
    # Implementa direttamente lo pseucodice dell'algoritmo EC
    def __init__(self, A, time_limit):
        self.__A = A
        self.__rows, self.cols = A.shape
        self.__COV = []
        self.__B = np.zeros((self.__rows, self.__rows), dtype=int)

        self.__zeros = np.zeros(self.cols, dtype=int)
        self.__ones = np.ones(self.cols, dtype=int)

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
