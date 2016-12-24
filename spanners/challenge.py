"""
This module is for loading and dumping data challenges.

A data challenge is a geometric spanner amidst an obstacle problem.

The format of a data challenge is as follows:
    - first line contains one integer: the number of points n
    - second line contains one integer: the number of vertices of the
      obstacle m
    - third line contains two positive integers a and b encoding the
      ratio t = a/b,
    - n lines contain two positive integers each: the two coordinates
      of an input point
    - m lines contain two positive integers each: the two coordinates
      of an obstacle vertex. The vertices should be given in clock-wise
      order along the polygonal obstacle

"""
from spanners import models


def load(fs):
    """
    Load a data challenge from a file stream.

    Args:
        fs (TextIOBase): The file stream from which to load the
            data challenge.

    Returns:
        Problem: The data challenge as a problem.

    Raises:
        FileFormatError: If the file stream cannot be loaded into a
            problem.

    """
    points = []
    obstacle = []
    n = int(fs.readline().strip())
    m = int(fs.readline().strip())
    a, b = (int(i) for i in fs.readline().strip().split())
    problem = models.Problem(points, obstacle, a, b)
    try:
        points = (
            models.Point(*map(int, fs.readline().split()))
            for i in range(m + n))
        for i in range(n):
            problem.points.append(next(points))
        for i in range(m):
            problem.obstacle.append(next(points))
    except TypeError as exc:
        raise FileFormatError('Expected another point.') from exc
    except ValueError as exc:
        raise FileFormatError(
            'Expected a point (i.e. <int><space><int>)') from exc
    if any(line.strip() for line in fs.readlines()):
        raise FileFormatError('Expected end of file.')
    return problem


def dump(problem, fs):
    """
    Dump a problem as a data challenge to a file stream.

    Args:
        problem (Problem): The problem to dump to a file.
        fs (TextIOBase): The filestream in which to dump the problem.

    """
    lines = []
    lines.append(str(len(problem.points)))
    lines.append(str(len(problem.obstacle)))
    lines.append('{} {}'.format(problem.a, problem.b))
    lines.extend('{} {}'.format(point.x, point.y) for point in problem)
    fs.write('\n'.join(lines) + '\n')


class FileFormatError(Exception):
    """
    Error to be raised if a file contains a format error.

    """
    pass
