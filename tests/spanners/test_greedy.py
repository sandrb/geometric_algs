#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.greedy` module.

"""
import pytest

from spanners import greedy


def test_compute_spanner(problem, solution):
    """
    Test for `greedy.compute_spanner`.

    Args:
        problem (Problem): The problem to test.
        solution (Solution): The expected solution

    """
    output = greedy.compute_spanner(problem)

    assert output == solution


if __name__ == '__main__':
    pytest.main(__file__)
