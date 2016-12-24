#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.visualizer` module.

"""
import pytest

from spanners import generator


def test_generate():
    """
    Test for `generator.generate`.

    """
    assert False  # TODO
    output = generator.generate(1000, 1000, 40, 20)
    assert output is not None


if __name__ == '__main__':
    pytest.main(__file__)
