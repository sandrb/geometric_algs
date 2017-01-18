"""
This module holds fixtures to be used by multiple modules for testing.

"""
import pytest

from spanners import models


@pytest.fixture
def problem():
    """
    Provide a problem.

    Returns:
        models.Problem: A problem.

    """
    points = [
        models.Point(42, 666),
        models.Point(666, 42),
    ]
    obstacle = [
        models.Point(0, 0),
        models.Point(0, 10),
        models.Point(10, 10),
        models.Point(10, 0),
    ]
    return models.Problem(points, obstacle, 314, 271)


@pytest.fixture
def edge():
    """
    Provide an edge.

    Returns:
        models.Edge: An edge.

    """
    return models.Edge(models.Point(42, 666), models.Point(666, 42))


@pytest.fixture
def solution(problem, edge):
    """
    Provide a solution.

    Args:
        problem (models.Problem): The problem o
        edge (models.Edge)

    Returns:
        models.Solution: A solution.

    """
    return models.Solution(problem, 1, 882.4692629208113, {edge})
