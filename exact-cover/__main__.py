"""main.py
Main function and the functions for the subcommands.
"""

import signal
import inst
from inst import rand, sudoku
import compare
import ec
import cli
import numpy as np

args = cli.get_args()

np.set_printoptions(linewidth=10000)


def __ec_cmd():
    input_matrix, is_sudoku, dim = inst.read_from_file(args.input)

    alg = None
    if args.plus:
        alg = ec.ECPlus(input_matrix, time_limit=args.time)
    else:
        alg = ec.EC(input_matrix, time_limit=args.time)

    signal.signal(signal.SIGINT, lambda *_: alg.stop())

    result = alg.start()
    ec.write_output(output_file=args.output, input_matrix=input_matrix,
                    result=result, is_sudoku=is_sudoku, dim=dim)

    print(f'Output file created at \"{args.output}\".')


def __gen_cmd():
    if args.subcommand == 'rand':
        instance = rand.gen_inst(args.mdim, args.ndim, args.prob, args.guarantee)
        rand.write_to_file(args.output, instance)
    elif args.subcommand == 'sudoku':
        instance = sudoku.gen_inst(args.side_dim, args.diff)
        sudoku.write_to_file(args.output, instance)

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
