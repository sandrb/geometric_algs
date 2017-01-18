#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.quadtrees` module.

"""
import pytest

from spanners import models
from spanners import quadtrees


@pytest.fixture
def bounding_box():
    """
    Provide a bounding box.

    Returns:
        quadtree.BoundingBox: A bounding box.

    """
    return quadtrees.BoundingBox(
        models.Point(0, 0),
        models.Point(16, 16))


@pytest.fixture
def points():
    """
    Provide a set of points.

    Based upon slide 31 of lecture 6.

    Returns:
        Set[Point]: A set of points.

    """
    return {
        models.Point(1, 14),  # a
        models.Point(7, 15),  # b
        models.Point(6, 13),  # c
        models.Point(14, 10),  # d
        models.Point(13, 3),  # e
    }


@pytest.fixture
def quadtree(points):
    """
    Provide a quadtree.

    Args:
        points (Set[model.Point]): The points for which to provide a
            quadtree.

    Returns:
        quadtrees.Quadtree: A quadtree.

    """
    return quadtrees.Quadtree(points)


class TestBoundingBox:
    """
    Test class for `quadtrees.BoundingBox`.

    """

    def _bounding_box(self):
        return bounding_box()

    def test___slots__(self, bounding_box):
        """
        Test for `BoundingBox.__slots__`.

        This should only contain the two points defining the bounding box
        for memory efficiency. There will be a lot of bounding boxes and
        this helps to reduce the memory footprint.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.__slots__ == ('lower_left', 'upper_right')

    def test_width(self, bounding_box):
        """
        Test for `BoundingBox.width`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.width == 16
        bounding_box.lower_left = models.Point(-3, -14)
        assert bounding_box.width == 19
        bounding_box.lower_left = models.Point(999, 999)
        assert bounding_box.width == 0

    def test_height(self, bounding_box):
        """
        Test for `BoundingBox.height`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.height == 16
        bounding_box.upper_right = models.Point(32, 42)
        assert bounding_box.height == 42
        bounding_box.upper_right = models.Point(-999, -999)
        assert bounding_box.height == 0

    def test_center(self, bounding_box):
        """
        Test for `BoundingBox.center`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.center == models.Point(8, 8)
        bounding_box.lower_left = models.Point(-3, -14)
        assert bounding_box.center == models.Point(6.5, 1)
        bounding_box.upper_right = models.Point(-999, -999)
        assert bounding_box.center == models.Point(-501, -506.5)

    def test_edge(self, bounding_box):
        """
        Test for `BoundingBox.edge`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.edge == models.Edge(
            models.Point(0, 0),
            models.Point(16, 16),
        )

    @pytest.mark.parametrize('i, expected', [
        (1, quadtrees.BoundingBox(models.Point(8, 8), models.Point(16, 16))),
        (2, quadtrees.BoundingBox(models.Point(0, 8), models.Point(8, 16))),
        (3, quadtrees.BoundingBox(models.Point(0, 0), models.Point(8, 8))),
        (4, quadtrees.BoundingBox(models.Point(8, 0), models.Point(16, 8))),
    ])
    def test_quadrant(self, bounding_box, i, expected):
        """
        Test for `BoundingBox.quadrant` with a valid quadrant.

        Args:
            bounding_box (BoundingBox): The bounding box to test.
            i (int): The quadrant for which to get the bounding box.
            expected (BoundingBox): The expected output.

        """
        output = bounding_box.quadrant(i)
        assert isinstance(output, quadtrees.BoundingBox)
        assert output.lower_left == expected.lower_left
        assert output.upper_right == expected.upper_right

    def test_quadrant_value_error(self, bounding_box):
        """
        Test for `BoundingBox.quadrant` with an invalid quadrant.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        with pytest.raises(ValueError) as ctx:
            bounding_box.quadrant(42)
        assert ctx.value.args == ('There are only four quadrants.',)

    @pytest.mark.parametrize('point, expected', [
        (models.Point(0, 0), True),
        (models.Point(0, 16), False),
        (models.Point(8, 8), True),
        (models.Point(8, 16), False),
        (models.Point(16, 16), False),
    ])
    def test___contains__(self, bounding_box, point, expected):
        """
        Test for `BoundingBox.__contains__`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.
            point (models.Point): The point to check whether it is
                contained  in the bounding box.
            expected (bool): The expected output.

        """
        assert (point in bounding_box) == expected

    def test___eq__(self, bounding_box):
        """
        Test for `BoundingBox.__eq__` against another bounding box.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        bb = self._bounding_box()
        assert bounding_box.__eq__(bb)
        bb.lower_left = models.Point(-3, -14)
        assert not bounding_box.__eq__(bb)

    def test___eq___not_implemented(self, bounding_box):
        """
        Test for `BoundingBox.__eq__` against a non bounding box.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        assert bounding_box.__eq__('bounding box string') == NotImplemented

    def test___hash__(self, bounding_box):
        """
        Test for `BoundingBox.__hash__`.

        There should also be no hash collision for swapped points.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        bb = self._bounding_box()
        assert hash(bounding_box) == hash(bb)
        bb.lower_left, bb.upper_right = bb.upper_right, bb.lower_left
        assert hash(bounding_box) != hash(bb)

    def test___repr__(self, bounding_box):
        """
        Test for `BoundingBox.__repr__`.

        Args:
            bounding_box (BoundingBox): The bounding box to test.

        """
        output = repr(bounding_box)
        assert output == 'BoundingBox(Point(x=0, y=0), Point(x=16, y=16))'


class TestQuadtree:
    """
    Test class for `quadtrees.Quadtree`.

    """

    def _quadtree(self, points):
        return quadtree(points)

    def test___slots__(self, quadtree):
        """
        Test for `Quadtree.__slots__`.

        This should only contain the fields specified below for memory
        efficiency. There will be a lot of quadtrees and this helps to
        reduce the memory footprint.

        Args:
            quadtree (Quadtree): The quadtree to test.

        """
        assert sorted(quadtree.__slots__) == [
            '_compressed', '_len',
            'bounding_box', 'level', 'ne', 'nw', 'point', 'se', 'sw',
        ]

    def test_compress(self, mocker, points):
        """
        Test for `Quadtree.compress`.

        It tests the situation before and after compressing.

        Args:
            points (Set[Point]): The points for which to create a
                compressed quadtree.

        """
        points.remove(models.Point(1, 14))  # remove a
        quadtree = quadtrees.Quadtree(points)

        assert self._is_uncompressed(quadtree)

        output = quadtree.compress()
        assert output is quadtree
        assert self._is_compressed(quadtree)

        # Compression only works once.
        output = quadtree.compress()
        assert output is quadtree
        assert self._is_compressed(quadtree)

        # Compresssion is not recalculated
        quadtree.ne = mocker.Mock()
        quadtree.nw = mocker.Mock()
        quadtree.sw = mocker.Mock()
        quadtree.se = mocker.Mock()

        output = quadtree.compress()
        assert output is quadtree

        assert not quadtree.ne.called
        assert not quadtree.nw.called
        assert not quadtree.sw.called
        assert not quadtree.se.called

    def _is_uncompressed(self, quadtree):
        assert self._is_root_and_ne_and_sw_and_se_correct(quadtree)

        # nw
        assert quadtree.nw.bounding_box == quadtrees.BoundingBox(
            models.Point(0, 8), models.Point(8, 16))
        assert quadtree.nw.level == 1
        assert quadtree.nw.point is None

        assert quadtree.nw.ne.bounding_box == quadtrees.BoundingBox(
            models.Point(4, 12), models.Point(8, 16))
        assert quadtree.nw.ne.level == 2
        assert quadtree.nw.ne.point is None

        assert self._is_point_b_and_point_c_correct(quadtree.nw.ne)
        assert quadtree.nw.ne.ne.level == 3
        assert quadtree.nw.ne.nw.level == 3
        assert quadtree.nw.ne.sw.level == 3
        assert quadtree.nw.ne.se.level == 3

        assert quadtree.nw.nw.bounding_box == quadtrees.BoundingBox(
            models.Point(0, 12), models.Point(4, 16))
        assert quadtree.nw.nw.level == 2
        assert quadtree.nw.nw.point is None
        assert self._is_leaf(quadtree.nw.nw)

        assert quadtree.nw.sw.bounding_box == quadtrees.BoundingBox(
            models.Point(0, 8), models.Point(4, 12))
        assert quadtree.nw.sw.level == 2
        assert quadtree.nw.sw.point is None
        assert self._is_leaf(quadtree.nw.sw)

        assert quadtree.nw.se.bounding_box == quadtrees.BoundingBox(
            models.Point(4, 8), models.Point(8, 12))
        assert quadtree.nw.se.level == 2
        assert quadtree.nw.se.point is None
        assert self._is_leaf(quadtree.nw.se)

        return True

    def _is_compressed(self, quadtree):
        assert self._is_root_and_ne_and_sw_and_se_correct(quadtree)

        # nw
        assert quadtree.nw.bounding_box == quadtrees.BoundingBox(
            models.Point(0, 8), models.Point(8, 16))
        assert quadtree.nw.level == 1
        assert quadtree.nw.point is None

        assert self._is_point_b_and_point_c_correct(quadtree.nw)
        assert quadtree.nw.ne.level == 2
        assert quadtree.nw.nw.level == 2
        assert quadtree.nw.sw.level == 2
        assert quadtree.nw.se.level == 2

        return True

    def _is_root_and_ne_and_sw_and_se_correct(self, quadtree):
        __tracebackhide__ = True

        # root
        assert quadtree.bounding_box == bounding_box()
        assert quadtree.level == 0
        assert quadtree.point is None

        # ne
        assert quadtree.ne.bounding_box == quadtrees.BoundingBox(
            models.Point(8, 8), models.Point(16, 16))
        assert quadtree.ne.level == 1
        assert quadtree.ne.point == models.Point(14, 10)  # d
        assert self._is_leaf(quadtree.ne)

        # sw
        assert quadtree.sw.bounding_box == quadtrees.BoundingBox(
            models.Point(0, 0), models.Point(8, 8))
        assert quadtree.sw.level == 1
        assert quadtree.sw.point is None
        assert self._is_leaf(quadtree.sw)

        # se
        assert quadtree.se.bounding_box == quadtrees.BoundingBox(
            models.Point(8, 0), models.Point(16, 8))
        assert quadtree.se.level == 1
        assert quadtree.se.point == models.Point(13, 3)  # e
        assert self._is_leaf(quadtree.se)

        return True

    def _is_point_b_and_point_c_correct(self, quadtree):
        __tracebackhide__ = True

        assert quadtree.ne.bounding_box == quadtrees.BoundingBox(
            models.Point(6, 14), models.Point(8, 16))
        assert quadtree.ne.point == models.Point(7, 15)  # b
        assert self._is_leaf(quadtree.ne)

        assert quadtree.nw.bounding_box == quadtrees.BoundingBox(
            models.Point(4, 14), models.Point(6, 16))
        assert quadtree.nw.point is None
        assert self._is_leaf(quadtree.nw)

        assert quadtree.sw.bounding_box == quadtrees.BoundingBox(
            models.Point(4, 12), models.Point(6, 14))
        assert quadtree.sw.point is None
        assert self._is_leaf(quadtree.sw)

        assert quadtree.se.bounding_box == quadtrees.BoundingBox(
            models.Point(6, 12), models.Point(8, 14))
        assert quadtree.se.point == models.Point(6, 13)  # c
        assert self._is_leaf(quadtree.se)

        return True

    def _is_leaf(self, quadtree):
        __tracebackhide__ = True

        assert quadtree.ne is None
        assert quadtree.nw is None
        assert quadtree.sw is None
        assert quadtree.se is None

        return True

    def test___eq__(self, quadtree, points):
        """
        Test for `Quadtree.__eq__` against another quadtree.

        Args:
            quadtree (Quadtree): The quadtree to test.
            points (Set[Point]): The points in the quadtree.

        """
        qt = self._quadtree(points)
        assert quadtree.__eq__(qt)
        qt.ne = None
        assert not quadtree.__eq__(qt)

    def test___eq___not_implemented(self, quadtree):
        """
        Test for `Quadtree.__eq__` against a non-quadtree.

        Args:
            quadtree (Quadtree): The quadtree to test.

        """
        assert quadtree.__eq__("quadtree string") == NotImplemented

    def test___hash__(self, quadtree, points):
        """
        Test for `Quadtree.__hash__`.

        There should also be no hash collision for swapped subtrees.

        Args:
            quadtree (Quadtree): The quadtree to test.
            points (Set[Point]): The points in the quadtree.

        """
        qt = self._quadtree(points)
        assert hash(quadtree) == hash(qt)
        qt.ne, qt.nw = qt.nw, qt.ne
        assert hash(bounding_box) != hash(qt)

    def test___iter__(self, quadtree, points):
        """
        Test for `Quadtree.__iter__`.

        Args:
            quadtree (Quadtree): The quadtree to test.
            points (Set[Point]): The points expected to be in the iterabe.

        """
        output = iter(quadtree)
        for point in output:
            points.remove(point)
        assert len(points) == 0

    def test___len__(self, quadtree, points):
        """
        Test for `Quadtree.__len__`.

        Args:
            quadtree (Quadtree): The quadtree to test.
            points (Set[models.Points]): The points in the quadtree.

        """
        assert len(quadtree) == len(points)

    def test___repr__(self, quadtree, bounding_box, points):
        """
        Test for `Quadtree.__repr__`.

        Args:
            quadtree (Quadtree): The quadtree to test.
            bounding_box (BoundingBox): The expected bounding box.
            points (Set[models.Points]): The expected points.

        """
        output = repr(quadtree)
        assert output == "Quadtree({0}, {1}, 0)".format(
            repr(points), repr(bounding_box))


if __name__ == '__main__':
    pytest.main(__file__)
