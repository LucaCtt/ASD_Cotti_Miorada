"""check.py
Utility functions to check the outputs of EC and EC plus algorithms.
"""

import numpy as np
from ec import ECResult


def compare_results(input_files: list) -> list:
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
        res = read_result(file_name)
        if res.execution_time < min_exec_time or min_exec_time == 0:
            min_exec_time = res.execution_time
            min_idx = idx

        if len(results) > 0 and not res == results[0]:
            all_equal = False

        results.append(res)


    return all_equal, min_exec_time, min_idx


def read_result(file_name: str) -> ECResult:
    """Reads the search result from a file.

    Args:
        file_name (str): The path of the file.

    Returns:
        ECResult: The search result.
    """
    stopped = False
    visited_count = 0
    execution_time = 0
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

            if ';;; Execution time' in line:
                time_str = line.split()[3]
                execution_time = float(time_str[:-1])
                continue

            if ';;; Exact Coverages' in line:
                for cov_line in file:
                    cov = list(list(map(int, cov_line[1:-2].split())))
                    coverages.append(cov)
                # Coverages are at the end of the file
                # so we can just stop iterating.
                break

    return ECResult(np.asarray(coverages, dtype=object), visited_count, execution_time, stopped)
