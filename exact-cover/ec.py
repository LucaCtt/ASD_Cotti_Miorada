""" ec.py
Implementation of the EC and EC plus algorithms,
along with the functions to read and write the input and output files.
"""

from datetime import datetime
from dataclasses import dataclass
import time
import numpy as np
from inst import sudoku


@dataclass
class Result:
    """Represents the results of the EC algorithm."""

    coverages: np.ndarray
    visited_nodes: int
    total_nodes: int
    execution_time: float
    stopped: bool
    time_limit_reached: bool
    plus: bool = False

    def __eq__(self, __o: object) -> bool:
        return np.array_equal(self.coverages, __o.coverages)\
            and self.visited_nodes == __o.visited_nodes\
            and self.total_nodes == __o.total_nodes

    def visited_percentage(self):
        """Return the percentage of visited nodes."""
        return round(self.visited_nodes / self.total_nodes * 100, 4)


class EC:  # pylint: disable=too-many-instance-attributes
    """The basic EC algorithm."""

    def __init__(self, input_matrix: np.ndarray, time_limit: float = None):
        # A
        self._input_matrix = input_matrix
        self._n, self._m = input_matrix.shape

        # B
        self._compat_matrix = np.zeros((self._n, self._n), dtype=int)

        # COV
        # List instead of numpy array because it is more efficient to append
        self._coverages = []

        self.__time_limit = time_limit

        # process_time() is used instead of time() because it is more precise,
        # as it measures the time spent by the process in the CPU.
        self.__start_time = time.process_time()

        # Array of 0 for checking if A[i] is equal to empty set.
        self.__zeros = np.zeros(self._m, dtype=int)

        # Array of 1 for checking if A[i] is equal to M.
        # A[i] = M if A[i] contains all 1.
        self.__ones = np.ones(self._m, dtype=int)

        # Flag for stopping the algorithm.
        self.__stop_flag = False

        # Node statistics
        self._visited_nodes = 0
        self._total_nodes = (2**self._n)-1

    def stop(self):
        """Stop the algorithm."""
        self.__stop_flag = True

    def start(self) -> Result:
        """Start the algorithm."""
        for i in range(self._n):
            if self.__should_stop():
                break

            self._visited_nodes += 1

            # If A[i] is empty, skip it.
            if np.array_equal(self._input_matrix[i], self.__zeros):
                continue

            # If A[i] is equal to M, add it to the coverages.
            if np.array_equal(self._input_matrix[i], self.__ones):
                self._coverages.append([i])
                continue

            # Iterate rows before A[i].
            for j in range(i):
                if self.__should_stop():
                    break

                self._visited_nodes += 1

                # If the rows have at least one element in common,
                # set the compatibility to 0.
                if np.bitwise_and(self._input_matrix[j], self._input_matrix[i]).any():
                    self._compat_matrix[j, i] = 0
                else:
                    indexes = np.array([i, j])
                    union_value = self._get_union_value(i, j)

                    # If the union of the two rows is equal to M,
                    # add the indexes to the coverages and set the compatibility to 0.
                    if self._compare_union_value(union_value):
                        self._coverages.append(indexes)
                        self._compat_matrix[j, i] = 0
                    else:
                        self._compat_matrix[j, i] = 1

                        # Sets compatible with A[i] and A[j].
                        inter = np.bitwise_and(
                            self._compat_matrix[0:j, i], self._compat_matrix[0:j, j])

                        # If there are compatible sets, explore them.
                        if np.any(inter != 0):
                            self.__esplora(indexes, union_value, inter)

        return Result(coverages=self._coverages,
                      visited_nodes=self._visited_nodes,
                      total_nodes=self._total_nodes,
                      execution_time=self.__execution_time(),
                      stopped=self.__stop_flag,
                      time_limit_reached=self.__time_limit_reached()
                      )

    def _get_union_value(self, i, j):
        return np.bitwise_or(self._input_matrix[i], self._input_matrix[j])

    def _compare_union_value(self, union_value):
        return np.array_equal(union_value, self.__ones)

    def _get_union_value_temp(self, union_value, k):
        return np.bitwise_or(union_value, self._input_matrix[k])

    def __esplora(self, indexes, union_value, inter):
        for k, _ in enumerate(inter):
            if self.__should_stop():
                break

            # NB: I cannot remove zero elements from inter
            # because I would lose information about the indexes.
            if inter[k] == 1:
                self._visited_nodes += 1

                # Try to add A[k] to the coverage.
                indexes_temp = np.append(indexes, k)
                union_value_temp = self._get_union_value_temp(union_value, k)

                if self._compare_union_value(union_value_temp):
                    self._coverages.append(indexes_temp)
                else:
                    inter_temp = np.bitwise_and(
                        inter[0:k], self._compat_matrix[0:k, k])
                    if np.any(inter_temp != 0):
                        self.__esplora(
                            indexes_temp, union_value_temp, inter_temp)

    def __execution_time(self) -> float:
        return time.process_time() - self.__start_time

    def __time_limit_reached(self) -> bool:
        if self.__time_limit is None:
            return False

        return self.__execution_time() > self.__time_limit

    def __should_stop(self) -> bool:
        if self.__stop_flag:
            return True

        return self.__time_limit_reached()


class ECPlus(EC):
    """Implementation of the EC plus algorithm.
    """

    def __init__(self, input_matrix: np.ndarray, time_limit: float = None):
        super().__init__(input_matrix, time_limit)
        self.__card = np.count_nonzero(input_matrix, axis=1)

    def start(self):
        result = super().start()
        result.plus = True
        return result

    def _get_union_value(self, i, j):
        return self.__card[i] + self.__card[j]

    def _compare_union_value(self, union_value):
        return union_value == self._m

    def _get_union_value_temp(self, union_value, k):
        return union_value + self.__card[k]


def write_output(output_file: str,
                 input_matrix: np.ndarray,
                 result: Result,
                 is_sudoku: bool = False,
                 dim: int = 0):
    """Writes the output of the EC algorithm to a file.

    Args:
        output_file (str): The path of the output file.
        input_matrix (np.ndarray): The input matrix.
        coverages (np.ndarray): The exact coverages found by the EC algorithm.
        visited_count (int): The number of nodes visited by the EC algorithm.
        execution_time (float): The execution time of the algorithm.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        exec_time_minutes = round(result.execution_time / 60, 3)

        file.write(
            f';;; EC Algorithm ({"Plus version" if result.plus else "Base version"})\n')
        file.write(f';;; Executed at: {datetime.today()}\n')
        file.write(
            f';;; Execution time: {result.execution_time}s ({exec_time_minutes} minutes) \n')
        file.write(f';;; Stopped: {result.stopped}\n')
        file.write(f';;; Time limit reached: {result.time_limit_reached}\n')
        file.write(f';;; Nodes visited: {result.visited_nodes}\n')
        file.write(f';;; Total nodes: {result.total_nodes}\n')
        file.write(
            f';;; Percentage of nodes visited: {result.visited_percentage()}%\n')
        file.write(';;;\n')

        if is_sudoku:
            file.write(';;; Sudoku solutions: \n')
            for coverage in result.coverages:
                solution = sudoku.Sudoku.from_cover(coverage, dim)
                file.write(sudoku.sudoku2str(solution, ";;; "))
                file.write('\n;;;\n')

        idx = 1
        for i in input_matrix:
            file.write(f';;; Set {idx:>3}: {np.array2string(i)}\n')
            idx += 1

        file.write(';;;\n')
        file.write(';;; Exact Coverages:\n')
        if result.coverages == []:
            file.write(';;; No coverage found.\n')
        else:
            for coverage in result.coverages:
                file.write(f'{coverage+1}\n')


def read_result(file_name: str) -> Result:
    """Reads the search result from a file.

    Args:
        file_name (str): The path of the file.

    Returns:
        ECResult: The search result.
    """
    stopped = False
    visited_count = 0
    total_nodes = 0
    execution_time = 0
    time_limit_reached = False
    coverages = []

    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            if ';;; Stopped' in line:
                if 'True' in line:
                    stopped = True
                continue

            if ';;; Nodes visited' in line:
                visited_count = int(line.split()[3])
                continue

            if ';;; Total nodes' in line:
                total_nodes = int(line.split()[3])
                continue

            if ';;; Execution time' in line:
                time_str = line.split()[3]
                execution_time = float(time_str[:-1])
                continue

            if ';;; Time limit reached' in line:
                time_limit_reached = bool(line.split()[4])
                continue

            if ';;; Exact Coverages' in line:
                for cov_line in file:
                    cov = list(list(map(int, cov_line[1:-2].split())))
                    coverages.append(cov)
                # Coverages are at the end of the file
                # so we can just stop iterating.
                break

    return Result(coverages=np.asarray(coverages, dtype=object),
                  visited_nodes=visited_count,
                  total_nodes=total_nodes,
                  execution_time=execution_time,
                  stopped=stopped,
                  time_limit_reached=time_limit_reached)
