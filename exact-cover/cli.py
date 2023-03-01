"""cli.py
Provides the cli for the program.
"""

import argparse

# Main parser
__parser = argparse.ArgumentParser(prog="exact-cover")
__subparser = __parser.add_subparsers(help='command help', dest='command')

# Parser for the ec subcommand
__parser_ec = __subparser.add_parser('ec',
                                     help='ec help',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__parser_ec.add_argument("-i",
                         "--input",
                         type=str,
                         help="Input file.",
                         default="test/in.txt")
__parser_ec.add_argument("-o",
                         "--output",
                         type=str,
                         help="Output file.",
                         default="test/out.txt")
__parser_ec.add_argument("-t",
                         "--time",
                         type=int,
                         help="Max execution time.",
                         default=None)
__parser_ec.add_argument("-p",
                         "--plus",
                         type=bool,
                         help="Use EC plus instead of basic algorithm.",
                         action=argparse.BooleanOptionalAction,
                         default=False)
__parser_ec.add_argument("-s",
                         "--sparse",
                         type=bool,
                         help="Use sparse matrix representation.",
                         action=argparse.BooleanOptionalAction,
                         default=False)
__parser_ec.add_argument("-k",
                         "--stack",
                         type=bool,
                         help="Use stack for indices.",
                         action=argparse.BooleanOptionalAction,
                         default=False)

# Parser for the gen subcommand
__parser_gen = __subparser.add_parser('gen',
                                      help='gen help',
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

__subparser_gen = __parser_gen.add_subparsers(help='command help',
                                              dest='subcommand')

# Parser for the random gen subcommand
__parser_rand = __subparser_gen.add_parser('rand',
                                             help='rand help',
                                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__parser_rand.add_argument("-o",
                          "--output",
                          type=str,
                          help="Output file.",
                          default="test/in.txt")
__parser_rand.add_argument("-m",
                             "--mdim",
                             type=int,
                             help="Number of elements in M.",
                             default=10)
__parser_rand.add_argument("-n",
                             "--ndim",
                             type=int,
                             help="Number of elements in N.",
                             default=10)
__parser_rand.add_argument("-p",
                             "--prob",
                             type=float,
                             help="Probability to generate a 1 in the binomial distribution.",
                             default=0.5)
__parser_rand.add_argument("-g",
                             "--guarantee",
                             type=bool,
                             help="Guarantee at least one solution exists.",
                             action=argparse.BooleanOptionalAction,
                             default=False)

# Parser for the sudoku gen subcommand
__parser_sudoku = __subparser_gen.add_parser('sudoku',
                                             help='sudoku help',
                                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__parser_sudoku.add_argument("-o",
                          "--output",
                          type=str,
                          help="Output file.",
                          default="test/in.txt")
__parser_sudoku.add_argument("-s",
                             "--side-dim",
                             type=int,
                             help="Dimension of the side of the sudoku.",
                             default=9)

__parser_sudoku.add_argument("-d",
                             "--diff",
                             type=float,
                             help="Difficulty of the sudoku puzzle, between 0 and 1.",
                             default=0.3)

# Parser for the compare subcommand
__parser_check = __subparser.add_parser('compare',
                                        help='compare help',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__parser_check.add_argument("-i",
                            "--input",
                            type=str,
                            nargs="+",
                            help="Input files.")


def get_args() -> argparse.Namespace:
    """Get the arguments from the cli.

    Returns:
        argparse.Namespace: the arguments parsed from the cli.
    """
    args = __parser.parse_args()
    if not args.command:
        __parser.error('No arguments provided.')

    return args
