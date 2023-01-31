"""cli.py
Provides the cli for the program.
"""

import argparse

__parser = argparse.ArgumentParser(prog="exact-cover")
__subp = __parser.add_subparsers(help='sub-command help', dest='command')

# Parser for the ec subcommand
__p_ec = __subp.add_parser('ec', help='ec help',
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__p_ec.add_argument("-i", "--input", type=str,
                        help="Input file.", default="test/in.txt")
__p_ec.add_argument("-o", "--output", type=str,
                        help="Output file.", default="test/out.txt")
__p_ec.add_argument("-t", "--time", type=int,
                        help="Max execution time.", default=None)
__p_ec.add_argument("-p", "--plus", type=bool, help="Use EC plus instead of basic algorithm.",
                        action=argparse.BooleanOptionalAction, default=False)

# Parser for the dlx subcommand
__p_dlx = __subp.add_parser('dlx', help='dlx help',
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__p_dlx.add_argument("-i", "--input", type=str,
                        help="Input file.", default="test/in.txt")
__p_dlx.add_argument("-o", "--output", type=str,
                        help="Output file.", default="test/out.txt")

# Parser for the gen subcommand
__p_gen = __subp.add_parser('gen', help='gen help',
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__p_gen.add_argument("-o", "--output", type=str,
                     help="Output file.", default="test/in.txt")
__p_gen.add_argument("-m", "--mdim", type=int,
                     help="Number of elements in M.", default=10)
__p_gen.add_argument("-n", "--ndim", type=int,
                     help="Number of elements in N.", default=10)
__p_gen.add_argument("-p", "--prob", type=float,
                     help="Probability to generate a 1 in the binomial distribution.", default=0.5)
__p_gen.add_argument("-g", "--guarantee", type=bool, help="Guarantee at least one solution exists.",
                        action=argparse.BooleanOptionalAction, default=False)

# Parser for the compare subcommand
__p_check = __subp.add_parser('compare', help='compare help',
                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
__p_check.add_argument("-i", "--input", type=str, nargs="+",
                       help="Input files.")


def get_args() -> argparse.Namespace:
    """Get the arguments from the cli.

    Returns:
        argparse.Namespace: the arguments parsed from the cli.
    """
    return __parser.parse_args()
