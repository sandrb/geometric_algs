"""
This module holds all domain models.

"""
import collections


Point = collections.namedtuple('Point', ['x', 'y'])
"""
type: A namedtuple that represents a 2D point.
"""


class Problem(collections.abc.Iterable):
    """
    This class represents a gemotric spanner problem.

    The general question of the problem is:  Given a set of points and
    an obstacle, how to construct a "good" network to connect the
    points while not passing through the obstacle.

    """

    def __init__(self, points, obstacle, a, b):
        """
        Initialize a `Problem`.

        Args:
            points (Collection[Point]): A collection of points for
                which to create a spanner.
            obstacle (Sequence[Point]): A sequence of points which
                represents an obstacle (i.e. a polygon).
            a (int): Numerator of the ratio to achieve for the problem.
            b (int): Denomenator of the ratio to achieve for the
                problem.

        """
        self.points = points
        self.obstacle = obstacle
        self.a = a
        self.b = b

    @property
    def ratio(self):
        """
        float: The ratio to achive for the problem.
        """
        return self.a / self.b

    def __iter__(self):
        """
        Get an iterator for all the points in the problem.

        Returns:
            Iterator[Point]: An iterator with all the points in the
                problem.

        """
        yield from self.points
        yield from self.obstacle
