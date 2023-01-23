import argparse
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(prog="EC")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_search = subparsers.add_parser('search', help='search help')
    parser_search.add_argument("-i", "--input", type=str,
                        help="File di input [in.txt]", default="in.txt")
    parser_search.add_argument("-o", "--output", type=str,
                        help="File di output [out.txt]", default="out.txt")
    parser_search.add_argument("-t", "--time", type=int,
                               help="Tempo massimo di esecuzione [infinito]", default=None)

    parser_gen = subparsers.add_parser('gen', help='gen help')
    parser_gen.add_argument("-o", "--output", type=str,
                        help="File di output [out.txt]", default="out.txt")
    parser_gen.add_argument("-m", "--mdim", type=int,
                            help="Numero di elementi in M", default=10)
    parser_gen.add_argument("-n", "--ndim", type=int,
                            help="Numero di elementi in N", default=10)
    parser_gen.add_argument("-p", "--prob", type=float,
                            help="Probabilità del binomiale", default=0.5)

    return parser.parse_args()

