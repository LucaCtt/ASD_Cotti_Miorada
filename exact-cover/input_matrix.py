"""input_matrix.py
Representations for the input matrix of the exact cover problem.
"""

from typing import Generic, Tuple, TypeVar
from abc import ABC, abstractmethod
import numpy as np
from scipy import sparse

T = TypeVar('T')


class InputMatrix(ABC, Generic[T]):
    """Represents a generic input matrix."""

    shape: Tuple[int, int]
    _input_matrix: T

    def __init__(self, input_matrix: T) -> None:
        super().__init__()
        self._input_matrix = input_matrix
        self.shape = input_matrix.shape

    @abstractmethod
    def row_empty(self, i: int) -> bool:
        """Check if a row of the matrix is empty.

        Args:
            i (int): The index of the row.

        Returns:
            bool: True if the row is empty, False otherwise.
        """
        pass

    @abstractmethod
    def row_full(self, i: int) -> bool:
        """Check if a row of the matrix is full of ones.

        Args:
            i (int): The index of the row.

        Returns:
            bool: True if the row is full, False otherwise.
        """
        pass

    @abstractmethod
    def intersection(self, i: int, array: T) -> Tuple[T, int]:
        """Computes the intersection between a row of the matrix and an array.

        Args:
            i (int): The index of the row.
            array (T): The array.

        Returns:
            Tuple[T, int]: The intersection and the number of ones in the intersection.
        """
        pass

    @abstractmethod
    def rows_intersection(self, i: int, j: int) -> Tuple[T, int]:
        """Computes the intersection between two rows of the matrix.

        Args:
            i (int): The index of the first row.
            j (int): THe index of the second row.

        Returns:
            Tuple[T, int]: The intersection and the number of ones in the intersection.
        """
        pass

    @abstractmethod
    def union(self, i: int, array: T) -> Tuple[T, int]:
        """Computes the union between a row of the matrix and an array.

        Args:
            i (int): The index of the row.
            array (T): The array.

        Returns:
            Tuple[T, int]: The union and the number of ones in the union.
        """
        pass

    @abstractmethod
    def rows_union(self, i: int, j: int) -> Tuple[T, int]:
        """Computes the union between two rows of the matrix.

        Args:
            i (int): The index of the first row.
            j (int): The index of the second row.

        Returns:
            Tuple[T, int]: The union and the number of ones in the union.
        """
        pass

    @abstractmethod
    def nonzero_per_col(self):
        pass
    

    def __iter__(self):
        return iter(self._input_matrix)


class SparseInputMatrix(InputMatrix[sparse.spmatrix]):
    """Represents a sparse input matrix."""

    def __init__(self, input_matrix: list) -> None:
        super().__init__(sparse.csr_matrix(input_matrix))

    def row_empty(self, i: int) -> bool:
        return self._input_matrix.getrow(i).nnz == 0

    def row_full(self, i: int) -> bool:
        return self._input_matrix.getrow(i).nnz == self._input_matrix.shape[1]

    def intersection(self, i: int, array: sparse.spmatrix) -> Tuple[sparse.spmatrix, int]:
        inter = self._input_matrix.getrow(i).multiply(array)
        return inter, inter.nnz

    def rows_intersection(self, i: int, j: int) -> Tuple[sparse.spmatrix, int]:
        return self.intersection(i, self._input_matrix.getrow(j))

    def union(self, i: int, array: sparse.spmatrix) -> Tuple[sparse.spmatrix, int]:
        union = self._input_matrix.getrow(i) + array
        return union, union.nnz

    def nonzero_per_col(self):
        return self._input_matrix.getnnz(axis=1)

    def rows_union(self, i: int, j: int) -> Tuple[sparse.spmatrix, bool]:
        return self.union(i, self._input_matrix.getrow(j))

    def __iter__(self):
        return iter(self._input_matrix.toarray())


class DenseInputMatrix(InputMatrix[np.ndarray]):
    """Represents a dense input matrix."""

    def __init__(self, input_matrix: list) -> None:
        super().__init__(np.array(input_matrix))

    def row_empty(self, i: int) -> bool:
        return not np.any(self._input_matrix[i])

    def row_full(self, i: int) -> bool:
        return np.all(self._input_matrix[i])

    def intersection(self, i: int, array: np.ndarray) -> Tuple[np.ndarray, int]:
        inter = np.bitwise_and(self._input_matrix[i], array)
        return inter, np.count_nonzero(inter)

    def rows_intersection(self, i: int, j: int) -> Tuple[np.ndarray, int]:
        return self.intersection(i, self._input_matrix[j])

    def union(self, i: int, array: np.ndarray) -> Tuple[np.ndarray, int]:
        union = np.bitwise_or(self._input_matrix[i], array)
        return union, np.count_nonzero(union)

    def nonzero_per_col(self):
        return np.count_nonzero(self._input_matrix, axis=1)

    def rows_union(self, i: int, j: int) -> Tuple[np.ndarray, int]:
        return self.union(i, self._input_matrix[j])
