#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.models` module.

"""
import pytest

from spanners import models


def test_point():
    """
    Test for `models.Point`.

    A point should be a 2-tuple.
    It should also have an x and y attribute.

    """
    point = models.Point(42, 666)
    assert point.x == 42
    assert point.y == 666
    assert point == (42, 666)


class TestProblem:
    """
    Test class for `models.Problem`.

    """
    def test_ratio(self, problem):
        """
        Test for `Problem.ratio`.

        Args:
            problem (Problem): The problem to test.

        """
        assert problem.ratio == 314 / 271

    @pytest.mark.parametrize('point, expected', [
        (models.Point(0, 0), True),
        (models.Point(42, 666), True),
        (models.Point(314, 271), False),
    ])
    def test___contains__(self, problem, point, expected):
        """
        Test for `Problem.__contains__`.

        Args:
            problem (Problem): The problem to test.
            point (Point): The point to test for containment in the
                problem.
            expected (bool): Whether the point is expected to be
                contained in the problem.

        """
        assert (point in problem) == expected

    def test___iter__(self, problem):
        """
        Test for `Problem.__iter__`.

        Args:
            problem (Problem): The problem to test.

        """
        iterator = iter(problem)
        expected = {
            models.Point(42, 666),
            models.Point(666, 42),
            models.Point(0, 0),
            models.Point(0, 10),
            models.Point(10, 10),
            models.Point(10, 0),
        }
        for i in range(len(expected)):
            point = next(iterator)
            assert point in expected
            expected.remove(point)

        with pytest.raises(StopIteration):
            next(iterator)

    def test___len__(self, problem):
        """
        Test for `Problem.__len__`.

        Args:
            problem (Problem): The problem to test.

        """
        assert len(problem) == 6

    def test___repr__(self, problem):
        """
        Test for `Problem.__repr__`.

        Args:
            problem (Problem): The problem to test.

        """
        assert repr(problem) == 'Problem('\
            '[Point(x=42, y=666), Point(x=666, y=42)], '\
            '[Point(x=0, y=0), Point(x=0, y=10), Point(x=10, y=10), '\
            'Point(x=10, y=0)], 314, 271)'


class TestEdge:
    """
    Test class for `models.Edge`.

    """

    def test___slots__(self, edge):
        """
        Test for `Edge.__slots__`.

        This should be an empty tuple for memory efficiency.
        There will be a lot of edges and this helps to reduce the
        memory footprint.

        Args:
            edge (Edge): The edge to test.

        """
        assert edge.__slots__ == ()

    def test_length(self, edge):
        """
        Test for `Edge.length`.

        Args:
            edge (Edge): The edge to test.

        """
        assert edge.length == 882.4692629208113
        point, __ = edge
        assert models.Edge(point, point).length == 0


class TestSolution:
    """
    Test class for `models.Solution`.

    """

    def test_density(self, solution):
        """
        Test for `Solution.density`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.density == 1.0

    def test_m_sparseness(self, solution):
        """
        Test for `Solution.m_sparseness`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.m_sparseness == 0.25

    def test_n_sparseness(self, solution):
        """
        Test for `Solution.n_sparseness`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.n_sparseness == 0.5

    def test_quality(self, solution):
        """
        Test for `Solution.quality`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.quality == 1.0

    def test_sparseness(self, solution):
        """
        Test for `Solution.sparseness`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.sparseness == 0.16666666666666666

    def test_weight(self, solution):
        """
        Test for `Solution.weight`.

        Args:
            solution (Solution): The solution to test.

        """
        assert solution.weight == 882.4692629208113

    def test___repr__(self, solution):
        """
        Test for `Solution.weight`.

        Args:
            solution (Solution): The solution to test.

        """
        assert repr(solution) == 'Solution(' \
            'Problem(' \
            '[Point(x=42, y=666), Point(x=666, y=42)], ' \
            '[Point(x=0, y=0), Point(x=0, y=10), Point(x=10, y=10), ' \
            'Point(x=10, y=0)], 314, 271), ' \
            '1, 882.4692629208113, ' \
            '{Edge({Point(x=666, y=42), Point(x=42, y=666)})})'


if __name__ == '__main__':
    pytest.main(__file__)
