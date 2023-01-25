""" Implementation of the EC and EC plus algorithms,
    along with the functions to read and write the input and output files.
"""

from datetime import datetime
import time
import numpy as np


class EC:  # pylint: disable=too-many-instance-attributes
    """The basic EC algorithm.
    """

    def __init__(self, input_matrix: np.ndarray, time_limit: float):
        self._input_matrix = input_matrix
        self._n, self._m = input_matrix.shape
        self._visited_count = 0
        self._coverages = []
        self._compat_matrix = np.zeros((self._n, self._n), dtype=int)

        self.__time_limit = time_limit
        self.__start_time = time.time()

        # Array of 0 for checking if A[i] is equal to empty set
        self.__zeros = np.zeros(self._m, dtype=int)

        # Array of 1 for checking if A[i] is equal to M
        # A[i] = M if A[i] contains all 1
        self.__ones = np.ones(self._m, dtype=int)

        # Flag for stopping the algorithm
        self.__stop_flag = False


    def stop(self):
        """Stop the algorithm.
        """
        self.__stop_flag = True

    def start(self):
        """Avvia l'algoritmo.
        """
        for i in range(0, self._n):
            if self._should_stop():
                break

            self._visited_count += 1

            if np.array_equal(self._input_matrix[i], self.__zeros):
                continue

            if np.array_equal(self._input_matrix[i], self.__ones):
                self._coverages.append([i])
                continue

            for j in range(0, i):
                if self._should_stop():
                    break

                self._visited_count += 1

                if np.bitwise_and(self._input_matrix[j], self._input_matrix[i]).any():
                    self._compat_matrix[j, i] = 0
                else:
                    self._verify_union(i, j)

        execution_time = time.time() - self.__start_time
        return self._coverages, self._visited_count, execution_time

    def _verify_union(self, i, j):
        indexes = np.array([i, j])
        union = np.bitwise_or(self._input_matrix[i], self._input_matrix[j])
        if np.array_equal(union, self.__ones):
            self._coverages.append(indexes)
            self._compat_matrix[j, i] = 0
        else:
            self._compat_matrix[j, i] = 1
            inter = np.bitwise_and(
                self._compat_matrix[0:j, i], self._compat_matrix[0:j, j])
            if inter.size > 0 and not np.array_equal(inter, np.zeros(inter.size, dtype=int)):
                self.__esplora(indexes, union, inter)

    def __esplora(self, indexes, union, inter):
        for k, _ in enumerate(inter):
            if self._should_stop():
                break

            self._visited_count += 1

            if inter[k] == 1:
                indexes_temp = np.append(indexes.copy(), k)
                union_temp = np.bitwise_or(union, self._input_matrix[k])

                if np.array_equal(union_temp, self.__ones):
                    self._coverages.append(indexes_temp)
                else:
                    inter_temp = np.bitwise_and(
                        inter[0:k], self._compat_matrix[0:k, k])
                    if inter_temp.size > 0 and not np.array_equal(inter_temp, np.zeros(inter_temp.size, dtype=int)):
                        self.__esplora(indexes_temp, union_temp, inter_temp)

    def _should_stop(self):
        if self.__stop_flag:
            return True

        if self.__time_limit is None:
            return False

        return time.time() - self.__start_time > self.__time_limit


class ECPlus(EC):
    """Implementation of the EC plus algorithm.
    """

    def __init__(self, input_matrix: np.ndarray, time_limit: float):
        super().__init__(input_matrix, time_limit)
        self.__card = np.zeros(self._n, dtype=int)

    def start(self):
        for i in range(0, self._n):
            self.__card[i] = np.count_nonzero(self._input_matrix[i])
        return super().start()

    def _verify_union(self, i, j):
        indexes = np.array([i, j])
        card_union = self.__card[i] + self.__card[j]
        if card_union == self._m:
            self._coverages.append(indexes)
            self._compat_matrix[j, i] = 0
        else:
            self._compat_matrix[j, i] = 1
            inter = np.bitwise_and(
                self._compat_matrix[0:j, i], self._compat_matrix[0:j, j])
            if inter.size > 0 and not np.array_equal(inter, np.zeros(len(inter), dtype=int)):
                self.__esplora_plus(indexes, card_union, inter)

    def __esplora_plus(self, indexes, card_union, inter):
        for k, _ in enumerate(inter):
            if self._should_stop():
                break

            self._visited_count += 1

            if inter[k] == 1:
                indexes_temp = np.append(indexes.copy(), k)
                card_temp = card_union + self.__card[k]

                if card_temp == self._m:
                    self._coverages.append(indexes_temp)
                else:
                    inter_temp = np.bitwise_and(
                        inter[0:k], self._compat_matrix[0:k, k])
                    if inter_temp.size > 0 and not np.array_equal(inter_temp, np.zeros(inter_temp.size, dtype=int)):
                        self.__esplora_plus(indexes_temp, card_temp, inter_temp)


def read_input(input_file: str) -> np.ndarray:
    """Reads an input matrix from a file.
    Refer to the documentation for the format of the input file.

    Args:
        input_file (str): The path of the input file.

    Returns:
        np.ndarray: The input matrix read from the file.
    """
    input_matrix = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            if ';;;' in line:
                continue
            if '-' in line:
                line = list(line.split())
                elements = []
                for element in line[0:-1]:
                    elements.append(int(element))
                input_matrix.append(elements)

    return np.array(input_matrix, dtype=int)


def write_output(
        output_file: str,
        input_matrix: np.ndarray,
        coverages: np.ndarray,
        visited_count: int,
        execution_time: float):
    """Writes the output of the EC algorithm to a file.

    Args:
        output_file (str): The path of the output file.
        input_matrix (np.ndarray): The input matrix.
        coverages (np.ndarray): The exact coverages found by the EC algorithm.
        visited_count (int): The number of nodes visited by the EC algorithm.
        execution_time (float): The execution time of the algorithm.
    """

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(';;; EC Algorithm \n')
        file.write(f';;; Executed at: {datetime.today()}\n')
        file.write(
            f';;; Execution time: {execution_time}s ({round(execution_time/60, 3)} minutes) \n')
        file.write(f';;; Nodes visited: {visited_count}\n')
        file.write(';;;\n')

        idx = 1
        for i in input_matrix:
            file.write(f';;; Set {idx}:\n{i}\n')
            idx += 1

        file.write(';;;\n')
        file.write(';;; Exact Coverages:\n')
        if coverages == []:
            file.write(';;; No coverage found.\n')
        else:
            for c in coverages:
                file.write(f'{c+1}\n')
