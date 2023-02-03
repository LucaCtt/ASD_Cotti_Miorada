"""gen.py
Generation of random instances for the EC problem.
"""

from dataclasses import dataclass
from datetime import datetime
import numpy as np
import sudoku as sk


@dataclass
class Instance:
    """Represents an instance of the EC problem."""
    input_matrix: np.ndarray
    gen_at: datetime = datetime.today()


@dataclass
class RandomInstance(Instance):
    """Represents a random instance of the EC problem."""
    prob: float = 0
    guarantee_sol: bool = False
    fixed_zero_col: bool = False


@dataclass
class SudokuInstance(Instance):
    """Represents a sudoku puzzle converted to an instance of the EC problem."""
    sudoku: sk.Sudoku = None
    difficulty: float = 0


def random_inst(card_m: int, card_n: int, prob: float, guarantee_sol: bool) -> RandomInstance:
    """Generates an instance of the EC problem.

    Args:
        card_m (int): The cardinality of set M.
        card_n (int): The cardinality of set N.
        prob (float): The probability of a bit to be 1.
        guarantee_sol (bool): True if the instance must have at least one solution.


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

    return RandomInstance(input_matrix=input_matrix,
                          prob=prob,
                          guarantee_sol=guarantee_sol,
                          fixed_zero_col=fixed_zero_col)


def sudoku_inst(dim=9, difficulty=0.3) -> SudokuInstance:
    """Generates a sudoku puzzle and converts it to an instance of the EC problem.

    Args:
        dim (int, optional): The dimension of the sudoku. Defaults to 9.

    Returns:
        SudokuInstance: The generated instance.
    """

    sudoku = sk.Sudoku(dim).gen_puzzle(difficulty)

    num_possibilities = dim ** 3  # 729 for a 9x9 board
    num_constraints = 4 * dim ** 2  # 324 for a 9x9 board

    input_matrix = np.zeros((num_possibilities, num_constraints), dtype=int)

    for row in range(sudoku.dim):
        for col in range(sudoku.dim):
            real_entry = sudoku.board[row, col]

            # If we don't already have an entry then all entries are possible.
            if real_entry == 0:
                possible_entries = range(1, sudoku.dim + 1)
            else:
                # If we already have an entry then leave out all the other possibilities.
                possible_entries = range(real_entry, real_entry + 1)

            for entry in possible_entries:
                __set_constraint_row(sudoku, input_matrix, row, col, entry)

    return SudokuInstance(input_matrix=input_matrix, sudoku=sudoku, difficulty=difficulty)


def __set_constraint_row(puzzle: sk.Sudoku,
                         constraints: np.ndarray,
                         row: int,
                         col: int,
                         entry: int) -> None:
    con_row = (row * puzzle.dim ** 2) + (col * puzzle.dim) + entry - 1
    cell_con_col = (0 * puzzle.dim ** 2) + (row * puzzle.dim) + col
    row_con_col = (1 * puzzle.dim ** 2) + (row * puzzle.dim) + entry - 1
    col_con_col = (2 * puzzle.dim ** 2) + (col * puzzle.dim) + entry - 1
    box_con_col = (
        (3 * puzzle.dim ** 2)
        + puzzle.dim * (puzzle.base * (row // puzzle.base) +
                        (col // puzzle.base))
        + entry
        - 1
    )

    constraints[con_row][cell_con_col] = 1
    constraints[con_row][row_con_col] = 1
    constraints[con_row][col_con_col] = 1
    constraints[con_row][box_con_col] = 1


def write_random_inst(output_file: str, inst: RandomInstance):
    """Writes an instance to a file.

    Args:
        output_file (str): The file where to write the instance.
        inst (Inst): The instance to write.
    """

    with open(output_file, 'w', encoding="utf-8") as file:
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


def write_sudoku_inst(output_file: str, inst: SudokuInstance):
    """Writes an instance to a file.

    Args:
        output_file (str): The file where to write the instance.
        inst (Inst): The instance to write.
    """

    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(f';;; Generated at: {inst.gen_at}\n')
        file.write(
            f';;; Difficulty: {inst.difficulty}\n')
        file.write(
            f';;; Sudoku: \n{inst.sudoku}')

        for row in inst.input_matrix:
            file.write(
                f'\n{np.array2string(row, max_line_width=999)[1:-1]} -')
