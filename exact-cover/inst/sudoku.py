"""sudoku.py
Generation of sudoku instances for the EC problem.
"""

from dataclasses import dataclass
from datetime import datetime
import math
import random
import numpy as np


@dataclass
class SudokuInstance:
    """Represents a sudoku puzzle converted to an instance of the EC problem."""

    input_matrix: np.ndarray
    sudoku: 'Sudoku'
    dim: int  # Puzzle dimension
    difficulty: float  # Between 0 and 1
    gen_at: datetime = datetime.today()


class Sudoku:  # pylint: disable=too-few-public-methods
    """Rappresents a Sudoku."""

    def __init__(self, dim: int, board: np.ndarray = None):
        # The sudoku has dimension dim x dim
        self.dim = dim

        # The sudoku is divided into base x base squares
        self.base = math.isqrt(dim)

        # The board is a dim x dim matrix
        self.board = board

        if self.board is None:
            self.__create_board()

    def gen_puzzle(self, difficulty: float) -> 'Sudoku':
        """Generates a puzzle from the board, by removing some cells.

        Args:
            difficulty (float, optional): The difficuly of the puzzle, from 0 to 1.
                                          The higher the difficulty, the more empty cells.

        Returns:
            Sudoku: The puzzle.
        """

        puzzle_board = self.board.copy()

        squares = self.dim**2
        num_empties = math.floor(squares * difficulty)

        # Remove cells by setting them to 0
        for cell in random.sample(range(squares), num_empties):
            puzzle_board[cell//self.dim][cell % self.dim] = 0

        return Sudoku(dim=self.dim, board=puzzle_board)

    @staticmethod
    def from_cover(cover: np.ndarray, dim: int) -> 'Sudoku':
        """Creates a Sudoku from an exact cover.

        Args:
            cover (np.ndarray): The exact cover.
            dim (int): The dimension of the sudoku.

        Returns:
            Sudoku: The sudoku of dimension dim x dim created from the cover.
        """

        cover.sort()
        board = np.fromiter(map(lambda x: (x % dim) + 1, cover), int).reshape(
            dim, dim
        )
        return Sudoku(dim=dim, board=board)

    def __create_board(self):
        # See https://stackoverflow.com/a/56581709

        self.board = np.zeros((self.dim, self.dim), dtype=int)

        def shuffle(population):
            return random.sample(population, len(population))

        def pattern(row, col):
            return (self.base * (row % self.base) + row // self.base + col) % self.dim

        base_range = range(self.base)

        rows = [(group * self.base + row)
                for group in shuffle(base_range) for row in shuffle(base_range)]
        cols = [(group * self.base + col)
                for group in shuffle(base_range) for col in shuffle(base_range)]
        nums = shuffle(list(range(1, self.dim + 1)))

        for row in rows:
            for col in cols:
                self.board[row][col] = nums[pattern(row, col)]


def gen_inst(dim: int, difficulty: float) -> SudokuInstance:
    """Generates a sudoku puzzle and converts it to an instance of the EC problem.

    Args:
        dim (int, optional): The dimension of the sudoku (dim x dim).
        diff (float, optional): The difficulty of the puzzle, between 0 and 1.

    Returns:
        SudokuInstance: The generated instance.
    """

    sudoku = Sudoku(dim).gen_puzzle(difficulty)

    num_possibilities = dim ** 3  # 729 for a 9x9 board
    num_constraints = 4 * dim ** 2  # 324 for a 9x9 board

    input_matrix = np.zeros((num_possibilities, num_constraints), dtype=int)

    for row in range(dim):
        for col in range(dim):
            real_entry = sudoku.board[row, col]

            # If we don't already have an entry then all entries are possible.
            if real_entry == 0:
                possible_entries = range(1, dim + 1)
            else:
                # If we already have an entry then leave out all the other possibilities.
                possible_entries = range(real_entry, real_entry + 1)

            for entry in possible_entries:
                __set_constraint_row(sudoku, input_matrix, row, col, entry)

    return SudokuInstance(input_matrix=input_matrix,
                          sudoku=sudoku,
                          dim=dim,
                          difficulty=difficulty)


def __set_constraint_row(puzzle: 'Sudoku',
                         constraints: np.ndarray,
                         row: int,
                         col: int,
                         entry: int):
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


def write_to_file(output_file: str, inst: SudokuInstance):
    """Writes an instance to a file.

    Args:
        output_file (str): The file where to write the instance.
        inst (Inst): The instance to write.
    """

    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(';;; Exact-Cover (Sudoku)\n')
        file.write(f';;; Generated at: {inst.gen_at}\n')
        file.write(
            f';;; Dimension: {inst.dim}\n')
        file.write(
            f';;; Difficulty: {inst.difficulty}\n')
        file.write(
            f';;; Sudoku puzzle: \n{sudoku2str(inst.sudoku, pre=";;; ")}')

        for row in inst.input_matrix:
            file.write(
                f'\n{np.array2string(row)[1:-1]} -')


def sudoku2str(sudoku: 'Sudoku', pre: str = '') -> str:
    """Converts a sudoku to a string.

    Args:
        sudoku (Sudoku): The sudoku to convert.
        pre (str, optional): String to append to the start of every new line. Defaults to ''.

    Returns:
        str: The sudoku as a string.
    """

    cell_length = len(str(sudoku.dim))
    format_int = '{0:0' + str(cell_length) + 'd}'
    rows = []

    for i, row in enumerate(sudoku.board):
        if i == 0:
            rows.append(pre)
            rows.append(('+-' + '-' * (cell_length + 1) *
                        sudoku.base) * sudoku.base + '+')

        rows.append(f'\n{pre}')
        rows.append((('| ' + '{} ' * sudoku.base) * sudoku.base + '|').format(*[format_int.format(
            x) if x != 0 else ' ' * cell_length for x in row]))

        if i == sudoku.dim - 1 or i % sudoku.base == sudoku.base - 1:
            rows.append(f'\n{pre}')
            rows.append(('+-' + '-' * (cell_length + 1) *
                        sudoku.base) * sudoku.base + '+')

    return ''.join(rows)
