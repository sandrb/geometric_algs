#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.generator` module.

"""
import pytest

from spanners import generator
from spanners import models


def test_generate():
    """
    Test for `generator.generate`.

    """
    assert False  # TODO
    output = generator.generate(1000, 1000, 40, 20)
    assert output is not None


@pytest.fixture
def obstacle(request):
    """
    Provide an obstacle.

    Returns:
        List[Point]: A list of points representing the obstacle.

    """
    return globals()[request.param + '_obstacle']()


@pytest.fixture
def complex_obstacle():
    """
    Provide a complex obstacle.

    Returns:
        List[Point]: A list of points representing the complex
            obstacle.

    """
    return [
        models.Point(346, 371),
        models.Point(263, 312),
        models.Point(60, 104),
        models.Point(352, 298),
        models.Point(95, 4),
        models.Point(288, 85),
        models.Point(332, 57),
        models.Point(565, 146),
        models.Point(777, 80),
        models.Point(640, 392),
        models.Point(764, 387),
        models.Point(851, 407),
        models.Point(760, 605),
        models.Point(958, 729),
        models.Point(823, 845),
        models.Point(674, 915),
        models.Point(463, 561),
        models.Point(163, 811),
        models.Point(55, 864),
        models.Point(79, 496),
    ]


@pytest.fixture
def triangle_obstacle():
    """
    Provide a triangle obstacle.

    Returns:
        List[Point]: A list of points representing the triangle
            obstacle.

    """
    return [
        models.Point(1, 1),
        models.Point(1, 3),
        models.Point(3, 1),
    ]


@pytest.mark.parametrize('point, obstacle, expected', [
    (models.Point(0, 0), 'complex', False),
    (models.Point(999, 999), 'complex', False),
    (models.Point(400, 600), 'complex', True),
    (models.Point(400, 605), 'complex', True),
    (models.Point(415, 600), 'complex', True),
    (models.Point(415, 605), 'complex', False),
    (models.Point(750, 600), 'complex', True),
    (models.Point(750, 605), 'complex', True),
    (models.Point(760, 600), 'complex', True),
    (models.Point(760, 605), 'complex', True),
    (models.Point(800, 600), 'complex', False),
    (models.Point(800, 605), 'complex', False),
    (models.Point(462, 387), 'complex', True),
    (models.Point(700, 387), 'complex', False),
    (models.Point(764, 387), 'complex', True),
    (models.Point(800, 387), 'complex', False),
    (models.Point(0, 0), 'triangle', False),
    (models.Point(0, 1), 'triangle', False),
    (models.Point(0, 2), 'triangle', False),
    (models.Point(0, 3), 'triangle', False),
    (models.Point(0, 4), 'triangle', False),
    (models.Point(1, 0), 'triangle', False),
    (models.Point(1, 1), 'triangle', True),
    (models.Point(1, 2), 'triangle', True),
    (models.Point(1, 3), 'triangle', True),
    (models.Point(1, 4), 'triangle', False),
    (models.Point(2, 0), 'triangle', False),
    (models.Point(2, 1), 'triangle', True),
    (models.Point(2, 2), 'triangle', True),
    (models.Point(2, 3), 'triangle', False),
    (models.Point(2, 4), 'triangle', False),
    (models.Point(3, 0), 'triangle', False),
    (models.Point(3, 1), 'triangle', True),
    (models.Point(3, 2), 'triangle', False),
    (models.Point(3, 3), 'triangle', False),
    (models.Point(3, 4), 'triangle', False),
    (models.Point(4, 0), 'triangle', False),
    (models.Point(4, 1), 'triangle', False),
    (models.Point(4, 2), 'triangle', False),
    (models.Point(4, 3), 'triangle', False),
    (models.Point(4, 4), 'triangle', False),
], indirect=['obstacle'])
def test__in_obstacle(point, obstacle, expected):
    """
    Test for `generator._in_obstacle`.

    Args:
        point (Point): The point to test whether it is in the obstacle.
        obstacle (Sequence[Point]): A sequnce of points representing
            the obstacle to test if the point is located in it.
        expected (bool): Whether the point is located in the obstacle.

    """
    assert generator._in_obstacle(point, obstacle) == expected


if __name__ == '__main__':
    pytest.main(__file__)
