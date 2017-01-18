"""
This module holds all domain models.

"""
import collections
import math


Point = collections.namedtuple('Point', ['x', 'y'])
"""
type: A namedtuple that represents a 2D point.
"""


class Problem(collections.abc.Collection):
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

    def __contains__(self, point):
        """
        Check whether the problem contains the given point.

        Args:
            point (Point): The point to check whether it is contained
                in the problem.

        Returns:
            bool: Whether the problem contains the given point.

        """
        return point in self.points or point in self.obstacle

    def __iter__(self):
        """
        Get an iterator for all the points in the problem.

        Returns:
            Iterator[Point]: An iterator with all the points in the
                problem.

        """
        yield from self.points
        yield from self.obstacle

    def __len__(self):
        """
        Get the number of points in the problem.

        Returns:
            int: The number of points in the problem.

        """
        return len(self.points) + len(self.obstacle)

    def __repr__(self):
        """
        Get the string representation of the problem.

        Returns:
            str: The string representation of the problem.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                self.points,
                self.obstacle,
                self.a,
                self.b,
            ])))


class Edge(frozenset):
    """
    This class represent an edge.

    """

    __slots__ = ()

    def __new__(cls, p, q):
        """
        Create an `Edge`.

        Args:
            p (Point): The first endpoint of the edge.
            q (Point): The other endpoint of the edge.

        """
        return super().__new__(cls, (p, q))

    @property
    def length(self):
        """
        Get the length of the edge.

        Returns:
            float: the length of the edge.

        """
        if len(self) == 2:
            p, q = self
            length = math.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)
        else:
            length = 0
        return length


class Solution(set):
    """
    This class represents a gemotric spanner solution.

    """

    def __init__(self, problem, max_edges, max_weight, edges=None):
        """
        Initialize a `Solution`.

        Args:
            problem (Problem): The problem to which the solution
                belongs.
            max_edges (int): The number of possible edges.
            max_weight (int): The sum of weights of the possible edges.

        Keyword Args:
            edges (Set[Edge]): The edges in the geometric spanner.
                Defaults to `None`.

        """
        super().__init__(edges or ())
        self.problem = problem
        self.max_edges = max_edges
        self.max_weight = max_weight

    @property
    def density(self):
        """
        float: The density of the solution.
        """
        return self.weight / self.max_weight

    @property
    def m_sparseness(self):
        """
        float: The m-sparseness of the solution.
        """
        return len(self) / len(self.problem.obstacle)

    @property
    def n_sparseness(self):
        """
        float: The n-sparseness of the solution.
        """
        return len(self) / len(self.problem.points)

    @property
    def quality(self):
        """
        float: The quality of the solution.
        """
        return len(self) / self.max_edges

    @property
    def sparseness(self):
        """
        float: The sparseness of the solution.
        """
        return len(self) / len(self.problem)

    @property
    def weight(self):
        """
        float: The weight of the result.
        """
        return sum(edge.length for edge in self)

    def __repr__(self):
        """
        Get the string representation of the problem.

        Returns:
            str: The string representation of the problem.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                self.problem,
                self.max_edges,
                self.max_weight,
                set(edge for edge in self),
            ])))
