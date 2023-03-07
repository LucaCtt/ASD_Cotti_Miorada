"""check.py
Utility functions to check the outputs of EC and EC plus algorithms.
"""

from typing import Tuple
import ec


def compare_results(input_files: list) -> Tuple[bool, float, int]:
    """Compares the EC results in the input files.
    Will return an error if the results are not equal, ie
    they refer to different problems.

    Args:
        input_files (list): The file containing the results to compare.

    Returns:
        bool: True if all the results are equal, False otherwise.
        float: The execution time of the fastest algorithm.
        int: The index of the fastest algorithm.
    """

    results = []
    all_equal = True
    min_exec_time = 0.0
    min_idx = 0

    for idx, file_name in enumerate(input_files):
        res = ec.read_result(file_name)
        if res.execution_time < min_exec_time or min_exec_time == 0:
            min_exec_time = res.execution_time
            min_idx = idx

        if len(results) > 0 and not res == results[0]:
            all_equal = False

        results.append(res)

    return all_equal, min_exec_time, min_idx
