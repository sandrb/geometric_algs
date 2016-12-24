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


if __name__ == '__main__':
    pytest.main(__file__)
