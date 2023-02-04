"""rand.py
Generation of random instances for the EC problem.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union
import numpy as np
from scipy import sparse


@dataclass
class RandomInstance:
    """Represents a random instance of the EC problem."""

    input_matrix: Union[np.ndarray, sparse.spmatrix]
    prob: float
    guarantee_sol: bool
    fixed_zero_col: bool
    gen_at: datetime = datetime.today()


def gen_inst(card_m: int,
             card_n: int,
             prob: float,
             guarantee_sol: bool,
             use_sparse: bool = False) -> RandomInstance:
    """Generates an instance of the EC problem.

    Args:
        card_m (int): The cardinality of set M.
        card_n (int): The cardinality of set N.
        prob (float): The probability of a bit to be 1. Must be between 0 and 1.
        guarantee_sol (bool): True if the instance must have at least one solution.
        use_sparse (bool): True if the instance must be represented as a sparse matrix. (default: False)


    Returns:
        Inst: The generated instance.
    """

    # There are at most 2^M unique rows,
    # so if N >= 2^M it is not possible to generate all different rows.
    if card_n >= 2**card_m:
        raise ValueError('N must be less than 2^M')

    input_matrix = np.empty((card_n, card_m), dtype=int)

    # Where to start the random generation.
    # If a solution must be guaranteed the first m rows
    # will contain an identity matrix,
    # so generation will start from the m+1 row.
    start_index = 0
    if guarantee_sol and card_m <= card_n:
        start_index = card_m
        input_matrix[0:card_m] = np.eye(card_m, dtype=int)

    for i in range(start_index, card_n):
        row = np.zeros(card_m, dtype=int)
        unique = False

        # Generates a random row until it is not empty
        # and also unique with respect to the already generated rows.
        while not row.any() or not unique:
            row = np.random.binomial(1, prob, card_m)

            unique = True
            # Iterate only on the already generated rows
            for element in input_matrix[0:i]:
                if (row == element).all():
                    unique = False

        input_matrix[i] = row

    fixed_zero_col = False
    # Check that there are no empty columns,
    # which would make the problem unsolvable.
    # If there are, for each empty column a random row is chosen
    # and the corresponding bit is set to 1.
    empty_idxs = np.argwhere(np.all(input_matrix[..., :] == 0, axis=0))
    if empty_idxs.size > 0:
        fixed_zero_col = True
        for idx in empty_idxs:
            input_matrix[np.random.randint(
                input_matrix.shape[0], size=1), idx] = 1

    return RandomInstance(input_matrix=sparse.csr_matrix(input_matrix) if use_sparse else input_matrix,
                          prob=prob,
                          guarantee_sol=guarantee_sol,
                          fixed_zero_col=fixed_zero_col)


def write_to_file(output_file: str, inst: RandomInstance):
    """Writes an instance to a file.

    Args:
        output_file (str): The file where to write the instance.
        inst (Inst): The instance to write.
    """

    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(';;; Exact-Cover (Random)\n')
        file.write(f';;; Generated at: {inst.gen_at}\n')
        file.write(
            f';;; Cardinality of M: {str(inst.input_matrix.shape[1])}\n')
        file.write(
            f';;; Cardinality of N: {str(inst.input_matrix.shape[0])}\n')
        file.write(f';;; Probability: {str(inst.prob)}\n')
        file.write(f';;; Guarantee solution: {str(inst.guarantee_sol)}\n')
        file.write(f';;; Fixed zero col: {str(inst.fixed_zero_col)}')

        for row in inst.input_matrix:
            file.write(f'\n{np.array2string(row)[1:-1]} -')


def read_from_file(input_file: str) -> RandomInstance:
    """Reads an instance from a file.

    Args:
        input_file (str): The file where to read the instance.

    Returns:
        Inst: The read instance.
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
