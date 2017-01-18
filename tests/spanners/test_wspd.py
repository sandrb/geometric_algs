#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.wspd` module.

"""
import pytest

from spanners import wspd


def test_compute_spanner(problem, solution):
    """
    Test for `wspd.compute_spanner`.

    Args:
        problem (Problem): The problem to test.
        solution (Solution): The expected solution

    """
    output = wspd.compute_spanner(problem)

    assert output == solution


if __name__ == '__main__':
    pytest.main(__file__)
