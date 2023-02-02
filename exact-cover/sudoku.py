"""sudoku.py
Sudoku generator.
"""
import math
import random
import numpy as np


class Sudoku:
    """Rappresents a Sudoku board."""

    def __init__(self, dim=9, board=None):
        self.__dim = dim
        self.__base = math.isqrt(dim)

        self.__board = self.__create_board() if board is None else board

    def gen_puzzle(self, difficulty: float = 0.7) -> np.ndarray:
        """Generates a puzzle from the board.

        Args:
            difficulty (float, optional): The difficuly of the puzzle, from 0 to 1.
                                          The higher the difficulty, the more empty cells.
                                          Defaults to 0.7.
        """
        puzzle_board = self.__board.copy()

        squares = self.__dim**2
        num_empties = math.floor(squares * difficulty)

        for cell in random.sample(range(squares), num_empties):
            puzzle_board[cell//self.__dim][cell % self.__dim] = 0

        return Sudoku(dim=self.__dim, board=puzzle_board)

    def __create_board(self):
        # See https://stackoverflow.com/a/56581709

        board = np.zeros((self.__dim, self.__dim), dtype=int)

        def shuffle(population):
            return random.sample(population, len(population))

        base_range = range(self.__base)

        rows = [(group * self.__base + row)
                for group in shuffle(base_range) for row in shuffle(base_range)]
        cols = [(group * self.__base + col)
                for group in shuffle(base_range) for col in shuffle(base_range)]
        nums = shuffle(list(range(1, self.__dim + 1)))

        for row in rows:
            for col in cols:
                board[row][col] = nums[self.__pattern(row, col)]

        return board

    def __pattern(self, row, col):
        return (self.__base * (row % self.__base) + row // self.__base + col) % self.__dim

    def __str__(self) -> str:
        table = ''
        cell_length = len(str(self.__dim))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(self.__board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.__base) * self.__base + '+' + '\n'
            table += (('| ' + '{} ' * self.__base) * self.__base + '|').format(*[format_int.format(
                x) if x != 0 else ' ' * cell_length for x in row]) + '\n'
            if i == self.__dim - 1 or i % self.__base == self.__base - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.__base) * self.__base + '+' + '\n'
        return table


if __name__ == '__main__':
    sudoku = Sudoku(9)
    print(sudoku)

    puzzle = sudoku.gen_puzzle(0.3)
    print(puzzle)
