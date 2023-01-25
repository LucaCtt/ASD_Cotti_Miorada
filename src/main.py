"""
Module for the main program.
Here you can find the main function and the functions for the subcommands.
"""

import argparse
import signal
from gen import gen_inst, write_inst
import ec

parser = argparse.ArgumentParser(prog="EC")
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

parser_search = subparsers.add_parser(
    'search', help='search help', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_search.add_argument("-i", "--input", type=str,
                           help="Input file.", default="test/in.txt")
parser_search.add_argument("-o", "--output", type=str,
                           help="Output file.", default="test/out.txt")
parser_search.add_argument("-t", "--time", type=int,
                           help="Max execution time.", default=None)
parser_search.add_argument("-p", "--plus",
                           type=int,
                           help="Use EC plus instead of basic algorithm.",
                           action=argparse.BooleanOptionalAction,
                           default=False)

parser_gen = subparsers.add_parser(
    'gen', help='gen help',  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_gen.add_argument("-o", "--output",
                        type=str,
                        help="Output file.",
                        default="test/in.txt")
parser_gen.add_argument("-m", "--mdim",
                        type=int,
                        help="Number of elements in M.",
                        default=10)
parser_gen.add_argument("-n", "--ndim",
                        type=int,
                        help="Number of elements in N.",
                        default=10)
parser_gen.add_argument("-p", "--prob",
                        type=float,
                        help="Probability to generate a 1 in the binomial distribution.",
                        default=0.5)

args = parser.parse_args()


def __search_cmd():
    input_matrix = ec.read_input(args.input)

    alg = None
    if args.plus:
        alg = ec.ECPlus(input_matrix, time_limit=args.time)
    else:
        alg = ec.EC(input_matrix, time_limit=args.time)

    signal.signal(signal.SIGINT, alg.stop)

    coverages, visited_count, execution_time = alg.start()

    ec.write_output(args.output, input_matrix, coverages,
                    visited_count, execution_time)

    print(f'Output file created at \"{args.output}\".')


def __gen_cmd():
    inst = gen_inst(args.mdim, args.ndim, args.prob)
    write_inst(args.output, inst)

    print(f'Instance created at \"{args.output}\".')


def __main():
    if args.command == 'search':
        __search_cmd()
    elif args.command == 'gen':
        __gen_cmd()


if __name__ == "__main__":
    __main()
