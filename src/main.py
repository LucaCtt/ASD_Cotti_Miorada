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

parser_gen = subparsers.add_parser(
    'gen', help='gen help',  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_gen.add_argument("-o", "--output", type=str,
                        help="Output file.", default="test/in.txt")
parser_gen.add_argument("-m", "--mdim", type=int,
                        help="Number of elements in M.", default=10)
parser_gen.add_argument("-n", "--ndim", type=int,
                        help="Number of elements in N.", default=10)
parser_gen.add_argument("-p", "--prob", type=float,
                        help="Probability to generate a 1 in the binomial distribution.", default=0.5)

args = parser.parse_args()


def search_cmd():
    A = ec.read_input(args.input)

    alg = ec.EC(A, args.time)
    signal.signal(signal.SIGINT, alg.stop)

    COV, visited_count, execution_time = alg.start()

    ec.write_output(args.output, A, COV, visited_count, execution_time)

    print(f'Output file created at \"{args.output}\".')


def gen_cmd():
    inst = gen_inst(args.mdim, args.ndim, args.prob)
    write_inst(args.output, inst)


def main():
    if args.command == 'search':
        search_cmd()
    elif args.command == 'gen':
        gen_cmd()


if __name__ == "__main__":
    main()
