"""
This module for constructing a compressed quadtree.

"""
import collections
import math

from spanners import models


def construct_compressed_quadtree(points):
    """
    Construct a compressed quadtree for the given points.

    Iterable[models.Point]: An interable of points for which to
        construct a compressed quadtree.

    Returns:
        Quadtree: The compressed quadtree.

    """
    return Quadtree(points).compress()


class BoundingBox(collections.abc.Container, collections.abc.Hashable):
    """
    This class represents a bounding box.

    """
    __slots__ = ('lower_left', 'upper_right')

    def __init__(self, lower_left, upper_right):
        """
        Initialize a `BoundingBox`.

        Args:
            lower_left (models.Point): The lower left corner of the
                bounding box.
            upper_right (models.Point): The upper right corner of the
                bounding box.

        """
        self.lower_left = lower_left
        self.upper_right = upper_right

    @property
    def width(self):
        """
        Real: The width of the bounding box.
        """
        return max(self.upper_right.x - self.lower_left.x, 0)

    @property
    def height(self):
        """
        Real: The height of the bounding box.
        """
        return max(self.upper_right.y - self.lower_left.y, 0)

    @property
    def center(self):
        """
        models.Point: The center of the bounding box.
        """
        return models.Point(
            (self.lower_left.x + self.upper_right.x) / 2,
            (self.lower_left.y + self.upper_right.y) / 2,
        )

    @property
    def edge(self):
        """
        models.Edge: The edge between the points defining the box.
        """
        return models.Edge(self.lower_left, self.upper_right)

    def quadrant(self, i):
        """
        Get the bounding box of the specified quadrant.

        Args:
            i: The quadrant for which to get the bounding box.

        Returns:
            BoundingBox: The bounding box of the specified quadrant.

        Raises:
            ValueError: If an invalid quadrant is specified.

        """
        if i == 1:
            quadrant = BoundingBox(
                models.Point(self.center.x, self.center.y),
                models.Point(self.upper_right.x, self.upper_right.y))
        elif i == 2:
            quadrant = BoundingBox(
                models.Point(self.lower_left.x, self.center.y),
                models.Point(self.center.x, self.upper_right.y))
        elif i == 3:
            quadrant = BoundingBox(
                models.Point(self.lower_left.x, self.lower_left.y),
                models.Point(self.center.x, self.center.y))
        elif i == 4:
            quadrant = BoundingBox(
                models.Point(self.center.x, self.lower_left.y),
                models.Point(self.upper_right.x, self.center.y))
        else:
            raise ValueError('There are only four quadrants.')
        return quadrant

    def __contains__(self, point):
        """
        Check whether the bounding box contains the given point.

        Args:
            point (models.Point): The point to check whether it is
                contained within the bounding box.

        Returns:
            bool: Whether the bounding box contains the given point.

        """
        return (
            self.lower_left.x <= point.x < self.upper_right.x and
            self.lower_left.y <= point.y < self.upper_right.y)

    def __eq__(self, other):
        """
        Check if two bounding boxes represent the same area.

        Args:
            other (BoundingBox): The other boundingbox to compare to.

        Returns:
            bool: Whether the two bounding boxes are equal or the
                singleton `NotImplemented` if the given argument is not
                a bounding box.

        """
        if isinstance(other, BoundingBox):
            result = (
                self.lower_left == other.lower_left and
                self.upper_right == other.upper_right)
        else:
            result = NotImplemented
        return result

    def __hash__(self):
        """
        Get the hash value of the bounding box.

        Returns:
            int: The hash value of the bounding box.

        """
        return hash((self.lower_left, self.upper_right))

    def __repr__(self):
        """
        Get the string representation of the bounding box.

        Retuns:
            str: The string representation of the bounding box.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                self.lower_left,
                self.upper_right,
            ])))


class Quadtree(collections.Iterable, collections.abc.Sized):
    """
    This class represents a quadtree.

    All points are stored in the leafs.

    """
    _child_names = ('ne', 'nw', 'sw', 'se')

    __slots__ = _child_names + (
        'bounding_box', 'level', 'point', '_compressed', '_len')

    def __init__(self, points, bounding_box=None, level=0):
        """
        Initialize a `Quadtree`.

        Args:
            points (Iterable[models.Point]): The points in the quadtree.

        Keyword Args:
            bounding_box (BoundingBox): The bounding box of the points
                in the quadtree. Only points in the bounding box are
                stored. If no bounding box is specified, then all
                points are considered. Defaults to `None`.
            level (int): The level of the quadtree. Defaults to zero.

        Note:
            Uses recursion.

        """
        self._compressed = False
        self.level = level
        if not bounding_box:
            points = set(points)
            self.bounding_box = self.__compute_bounding_box(points)
        else:
            self.bounding_box = bounding_box
            points = set(p for p in points if p in self.bounding_box)

        self._len = len(points)
        self.point = points.pop() if len(points) == 1 else None

        if len(points) <= 1:
            self.ne = None
            self.nw = None
            self.sw = None
            self.se = None
        else:
            for i, field in enumerate(self._child_names):
                setattr(
                    self, field, Quadtree(
                        points,
                        self.bounding_box.quadrant(i + 1),
                        self.level + 1))

    def __compute_bounding_box(self, points):
        greatest_number = max(
            (i for point in points for i in point), default=0)
        size = 2 ** math.ceil(math.log(greatest_number + 1, 2))
        return BoundingBox(models.Point(0, 0), models.Point(size, size))

    def compress(self):
        """
        Compress the quadtree.

        Returns:
            Quadtree: The quadtree itself, which is now compressed.

        Note:
            Uses recursion.

        """
        if not self._compressed:
            self._compressed = True

            for field in self._child_names:
                child = getattr(self, field)
                if child and len(self) == len(child):
                    for f in self._child_names:
                        setattr(self, f, getattr(child, f))
                        setattr(getattr(self, f), 'level', child.level)
                    # Holds at most once; points are split over quadrants.
                    break

            for field in self._child_names:
                child = getattr(self, field)
                if child:
                    child.compress()
        return self

    def __eq__(self, other):
        """
        Check if two quadtrees are equal.

        Args:
            other (BoundingBox): The other quadtree to compare to.

        Returns:
            bool: Whether the two quadtrees are equal or the singleton
                `NotImplemented` if the given argument is not a
                quadtree.

        """
        if isinstance(other, Quadtree):
            result = (
                self.level == other.level and
                self.bounding_box == other.bounding_box and
                self.ne == other.ne and
                self.nw == other.nw and
                self.sw == other.sw and
                self.se == other.se)
        else:
            result = NotImplemented
        return result

    def __hash__(self):
        """
        Get the hash value of the quadtree.

        Returns:
            int: The hash value of the quadtree.

        """
        return hash((
            self.level,
            self.bounding_box,
            self.ne,
            self.nw,
            self.sw,
            self.se,
        ))

    def __iter__(self):
        """
        Get an iterator for all the points stored in the quadtree.

        Returns:
            Iterator[Point]: An iterator with all the points stored in
                the quadtree.

        """
        if self.point:
            yield self.point
        else:
            for child_name in self._child_names:
                child = getattr(self, child_name)
                if child:
                    yield from child

    def __len__(self):
        """
        Get the number of points in the quadtree.

        Returns:
            int: The number of points in the quadtree.

        """
        return self._len

    def __repr__(self):
        """
        Get the string representation of the quadtree.

        Retuns:
            str: The string representation of the quadtree.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                set(self),
                self.bounding_box,
                self.level,
            ])))
