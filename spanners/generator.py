"""
This module is for generating problems.

TODO:
    https://stackoverflow.com/questions/14263284/create-non-intersecting-polygon-passing-through-all-given-points
    https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon


"""
import math
import random

from spanners import models


def generate(max_x, max_y, n, m, seed=None, polygonizer=None):
    """
    Generate a problem.

    Args:
        max_x (int): The upper limit of an x-coordinate that can be
            generated. Must be positive.
        max_y (int): The upper limit of a y-coordinate that can be
            generated. Must be positive.
        n (int): The number of points to generate. Must be positive.
        m (int): The number of points to generate which define the
            obstacle. Must be positive.

    Keyword Args:
        seed (int): The seed to use for the random generator.
        polygonizer (int): The polygonizer to use. Either `1` or `2`.
            Defaults to `2`.

    Raises:
        ValueError: If one of the arguments is not positive or if an
            invalid polygonizer is specified.

    """
    if max_x <= 0:
        raise ValueError(
            'The upper limit of an x-coordinate must be positive', max_x)
    if max_y <= 0:
        raise ValueError(
            'The upper limit of an y-coordinate must be positive', max_y)
    if n <= 0:
        raise ValueError(
            'The number of points to generate must be positive', n)
    if m <= 0:
        raise ValueError(
            'The number of points defining the obstacle must be positive', m)

    if polygonizer is not None:
        if polygonizer not in [1, 2]:
            raise ValueError(
                'polygonizer must be one of the following: {}'.format([1, 2]))

    obstacle = _generate_simple_polygon(max_x, max_y, m, seed)
    points = _generate_points(max_x, max_y, n, obstacle, seed)
    problem = models.Problem(points, obstacle, -1, -1)  # TODO: ratio
    return problem


def _generate_simple_polygon(max_x, max_y, m, seed=None, polygonizer=None):
    if polygonizer == 1:
        _convert_to_simple_polygon = _convert_to_simple_polygon_1
    else:
        _convert_to_simple_polygon = _convert_to_simple_polygon_2
    points = _generate_points(max_x, max_y, m, None, seed)
    points = _convert_to_simple_polygon(points)
    return points


def _generate_points(max_x, max_y, n, obstacle=None, seed=None):
    points = []
    unique_points = set()
    for i in range(n):
        point = _generate_point(max_x, max_y, unique_points, obstacle)
        points.append(point)
        unique_points.add(point)
    return points


def _generate_point(x_max, y_max, unique_points, obstacle=None):
    found_point = False
    while not found_point:
        x = random.randrange(x_max + 1)
        y = random.randrange(y_max + 1)
        point = models.Point(x, y)
        in_obstacle = obstacle is not None and _in_obstacle(point, obstacle)
        if point not in unique_points and not in_obstacle:
            found_point = True
    return point


def _in_obstacle(point, obstacle):
    # TODO: not yet peferfect
    intersections = 0
    previous_point = obstacle[-1]
    for current_point in obstacle:
        if previous_point.y - current_point.y != 0:
            if previous_point.x >= point.x and current_point.x >= point.x:
                if (previous_point.y <= point.y <= current_point.y or
                        previous_point.y >= point.y >= current_point.y):
                    intersections += 1
        previous_point = current_point
    return intersections % 2 == 1


def _convert_to_simple_polygon_1(points):
    # TODO: does not work correctly
    points.sort()
    left = points[0]
    right = points[-1]
    above = []
    below = []
    a = (right.y - left.y) / (right.x - left.x)  # slope
    b = left.y - a * left.x
    for point in points[1: -1]:
        if point.y < a * point.x + b:
            below.append(point)
        else:
            above.append(point)
    return [left] + above + [right] + below.reverse()


def _convert_to_simple_polygon_2(points):
    sum_x = sum(point.x for point in points)
    sum_y = sum(point.y for point in points)
    average_x = sum_x / len(points)
    average_y = sum_y / len(points)
    angles = []
    for point in points:
        dx = point.x - average_x
        dy = point.y - average_y
        angle = math.atan2(dy, dx)
        angles.append(angle)
    return [point for angle, point in sorted(zip(angles, points))]
