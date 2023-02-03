#!/usr/bin/env python3

"""main.py: Module for the main program.
Main function and the functions for the subcommands.
"""

import signal
import gen
import compare
import ec
import cli

args = cli.get_args()


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

    print(f'Output file created at \"{args.output}\".')


def __gen_cmd():
    if args.subcommand == 'random':
        inst = gen.random_inst(args.mdim, args.ndim, args.prob, args.guarantee)
        gen.write_random_inst(args.output, inst)
    elif args.subcommand == 'sudoku':
        inst = gen.sudoku_inst(args.side_dim, args.diff)
        gen.write_sudoku_inst(args.output, inst)

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
