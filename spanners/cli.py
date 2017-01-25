#!/usr/bin/env python3.6
"""
Calculate geometric spanners amidst obstacles.

Usage:
    {exec} generate X Y N M [-s SEED] FILE_OUT [-p POLY]
    {exec} solve [-a ALGO] FILE_IN [FILE_OUT]
    {exec} render (problem | solution [-a ALGO] [-c]) FILE_IN [FILE_OUT]
    {exec} show (problem | solution [-a ALGO] [-c]) FILE_IN
    {exec} (-h | --help)
    {exec} (-V | --version)

Arguments:
    FILE_IN
        The input file.

    FILE_OUT
        The output file.

    M
        The number of points to generate which define the obstacle.

    N
        The number of points to generate.

    X
        The upper limit of an x-coordinate that can be generated.

    Y
        The upper limit of a y-coordinate that can be generated.

Options:
    -a ALGO, --algorithm ALGO
        The algorithm to use for computing the solution.

    -c, --compute
        Compute the solution for visualization.

    -h, --help
        Show this screen.

    -p POLY, --polygonizer POLY
        The polygonization method to use. Either 1 or 2.

    -s SEED, --seed SEED
        The seed (integer) to use for the generator.

    -V, --version
        Show version.

"""
import sys

import docopt

import spanners
from spanners import service


def main():
    """
    Calculate geometric spanners amidst obstacles.

    Keyword Args:
        argv List[str]: List of arguments used to invoke the program with.
        Defaults to `sys.argv`.

    Raises:
        ValueError: If M, N, X, Y, POLY or SEED is not an integer.

    """
    doc = __doc__.format(exec=sys.argv[0])
    args = docopt.docopt(doc, version=spanners.__version__)
    if args['generate']:
        x = int(args['X'])
        y = int(args['Y'])
        n = int(args['N'])
        m = int(args['M'])

        seed = args['--seed']
        if seed is not None:
            seed = int(seed)

        polygonizer = args['--polygonizer']
        if polygonizer is not None:
            polygonizer = int(polygonizer)

        service.generate(
            x, y, n, m,
            seed=seed, filename=args['FILE_OUT'], polygonizer=polygonizer)
    elif args['solve']:
        service.solve(args['FILE_IN'], args['--algorithm'], args['FILE_OUT'])
    elif args['render'] and args['problem']:
        service.render_problem(args['FILE_IN'], args['FILE_OUT'])
    elif args['render'] and args['solution']:
        service.render_solution(
            args['FILE_IN'], args['--algorithm'], args['--compute'],
            args['FILE_OUT'])
    elif args['show'] and args['problem']:
        service.show_problem(args['FILE_IN'])
    elif args['show'] and args['solution']:
        service.show_solution(
            args['FILE_IN'], args['--algorithm'], args['--compute'])
    else:  # pragma: no cover
        raise SystemExit(docopt.printable_usage(doc))


if __name__ == '__main__':  # pragma: no cover
    main()
