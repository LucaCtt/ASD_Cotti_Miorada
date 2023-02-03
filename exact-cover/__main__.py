#!/usr/bin/env python3

"""main.py: Module for the main program.
Main function and the functions for the subcommands.
"""

import signal
from inst import rand, sudoku
import compare
import ec
import cli
import numpy as np

args = cli.get_args()

np.set_printoptions(linewidth=10000)


def __ec_cmd():
    input_matrix = ec.read_input(args.input)

    alg = None
    if args.plus:
        alg = ec.ECPlus(input_matrix, time_limit=args.time)
    else:
        alg = ec.EC(input_matrix, time_limit=args.time)

    signal.signal(signal.SIGINT, lambda *_: alg.stop())

    result = alg.start()
    ec.write_output(args.output, input_matrix, result)
    print(sudoku.sudoku_to_str(
        sudoku.Sudoku.from_cover(result.coverages[0], 4)))

    print(f'Output file created at \"{args.output}\".')


def __gen_cmd():
    if args.subcommand == 'rand':
        inst = rand.gen(args.mdim, args.ndim, args.prob, args.guarantee)
        rand.write_to_file(args.output, inst)
    elif args.subcommand == 'sudoku':
        inst = sudoku.gen(args.side_dim, args.diff)
        sudoku.write_to_file(args.output, inst)

    print(f'Instance created at \"{args.output}\".')


def __compare_cmd():
    all_equal, min_exec_time, min_exec_idx = compare.compare_results(
        args.input)

    if not all_equal:
        print('The results NOT are equal.')
    else:
        print('The results are equal.')
        print(
            f'Fastest was {args.input[min_exec_idx]} with execution time: {min_exec_time}')


if __name__ == "__main__":
    if args.command == 'ec':
        __ec_cmd()
    elif args.command == 'gen':
        __gen_cmd()
    elif args.command == 'compare':
        __compare_cmd()
