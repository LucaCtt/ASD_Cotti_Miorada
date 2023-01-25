""" generate.py
Generation of instances for the EC problem.
"""

from datetime import datetime
from dataclasses import dataclass
import numpy as np


@dataclass
class Inst:
    """Represents an instance of the EC problem."""
    input_matrix: np.ndarray
    prob: float
    gen_at: datetime = datetime.today()


def gen_inst(card_m: int, card_n: int, prob: float) -> Inst:
    """Generates an instance of the EC problem.

    Args:
        card_m (int): The cardinality of set M.
        card_n (int): The cardinality of set N.
        prob (float): The probability of a bit to be 1.

    Raises:
        ValueError: _description_

    Returns:
        Inst: _description_
    """

    # Esistono al più 2^M righe uniche,
    # quindi se N >= 2^M non è possibile generare righe tutte diverse
    if card_n >= 2**card_m:
        raise ValueError('N must be less than 2^M')

    input_matrix = np.empty((card_n, card_m), dtype=int)

    for i in range(0, card_n):
        row = np.zeros(card_m, dtype=int)
        unique = False

        # Genera una riga casuale finchè non è sia non vuota
        # (almeno un elemento diverso da zero)
        # sia unica rispetto alle righe già generate
        while not row.any() or not unique:
            row = np.random.binomial(1, prob, card_m)

            unique = True
            # Itera solo sulle righe già generate
            for element in input_matrix[0:i]:
                if (row == element).all():
                    unique = False

        input_matrix[i] = row

    return Inst(input_matrix, prob)


def write_inst(output_file: str, inst: Inst):
    """Writes an instance to a file.

    Args:
        output_file (str): The file where to write the instance.
        inst (Inst): The instance to write.
    """

    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(f';;; Generated at: {inst.gen_at}\n')
        file.write(f';;; Cardinality of M: {str(inst.input_matrix.shape[1])}\n')
        file.write(f';;; Cardinality of N: {str(inst.input_matrix.shape[0])}\n')
        file.write(f';;; Probability: {str(inst.prob)}')

        for row in inst.input_matrix:
            file.write(f'\n{np.array2string(row)[1:-1]} -')
