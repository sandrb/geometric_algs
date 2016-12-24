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
