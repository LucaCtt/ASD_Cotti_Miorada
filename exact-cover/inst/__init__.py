"""inst
Generation of instances for the exact cover problem.
"""

from typing import Tuple
from numpy import np


def read_from_file(input_file: str) -> Tuple[np.ndarray, bool, int]:
    """Reads an input matrix from a file.
    Refer to the documentation for the format of the input file.

    Args:
        input_file (str): The path of the input file.

    Returns:
        np.ndarray: The input matrix read from the file.
    """

    input_matrix = []
    is_sudoku = False
    dim = 0

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            if 'Sudoku' in line:
                is_sudoku = True
                continue

            if 'Dimension' in line:
                dim = int(line.split()[-1])
                continue

            if ';;;' in line:
                continue

            if '-' in line:
                line = list(line.split())
                elements = []
                for element in line[0:-1]:
                    elements.append(int(element))
                input_matrix.append(elements)

    return np.array(input_matrix, dtype=int), is_sudoku, dim
