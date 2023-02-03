"""sudoku.py
Sudoku puzzle generator.
"""

import math
import random
import numpy as np


class Sudoku:
    """Rappresents a Sudoku puzzle."""

    def __init__(self, dim=9, board=None):
        # The sudoku has dimension dim x dim
        self.dim = dim
        self.base = math.isqrt(dim)

        self.board = self.__create_board() if board is None else board

    def gen_puzzle(self, difficulty: float) -> 'Sudoku':
        """Generates a puzzle from the board.

        Args:
            difficulty (float, optional): The difficuly of the puzzle, from 0 to 1.
                                          The higher the difficulty, the more empty cells.
        """
        puzzle_board = self.board.copy()

        squares = self.dim**2
        num_empties = math.floor(squares * difficulty)

        for cell in random.sample(range(squares), num_empties):
            puzzle_board[cell//self.dim][cell % self.dim] = 0

        return Sudoku(dim=self.dim, board=puzzle_board)

    def __create_board(self):
        # See https://stackoverflow.com/a/56581709

        board = np.zeros((self.dim, self.dim), dtype=int)

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
                board[row][col] = nums[pattern(row, col)]

        return board

    def __str__(self) -> str:
        table = ''
        cell_length = len(str(self.dim))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(self.board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.base) * self.base + '+' + '\n'
            table += (('| ' + '{} ' * self.base) * self.base + '|').format(*[format_int.format(
                x) if x != 0 else ' ' * cell_length for x in row]) + '\n'
            if i == self.dim - 1 or i % self.base == self.base - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.base) * self.base + '+' + '\n'
        return table
