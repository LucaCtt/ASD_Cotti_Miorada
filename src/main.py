from gen import gen_inst, write_inst
import util
from search import search

args = util.get_args()


def search_cmd():
    search.start(args.input, args.output, args.time)


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
