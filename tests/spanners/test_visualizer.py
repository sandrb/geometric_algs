#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.visualizer` module.

"""
import matplotlib.pyplot as plt
import pytest

from spanners import visualizer


@pytest.fixture
def m_plt(mocker):
    """
    Provide a mock for `matplotlib.pyplot`.

    Returns:
        MagicMock: A mock for `matplotlib.pyplot`.

    """
    m_plt = mocker.patch('spanners.visualizer.plt')
    m_fig = mocker.MagicMock(spec=plt.Figure)
    m_ax = mocker.MagicMock(spec=plt.Axes)

    m_plt.subplots.return_value = m_fig, m_ax
    return m_plt


@pytest.mark.parametrize('filename, filetype, expected', [
    ('image', None, 'image.png'),
    ('image', 'png', 'image.png'),
    ('image.jpg', None, 'image.jpg.png'),
    ('image.jpg', 'png', 'image.jpg.png'),
    ('image.png', 'png', 'image.png'),
])
def test_vizualize_problem(m_plt, problem, filename, filetype, expected):
    """
    Test for `visualizer.vizualize_problem`.

    Args:
        m_plt (MagicMock): A mock for `matplotlib.pyplot`.
        problem (models.Problem): The problem to test.
        filename (str): The filename to use for the image of the
            problem.
        filetype (str): The filetype of the image.

    """
    output = visualizer.vizualize_problem(problem, filename, filetype)
    assert output is None

    m_fig, m_ax = m_plt.subplots.return_value

    assert m_fig.call_count == 0

    assert m_plt.Polygon.call_count == 1
    assert m_plt.Polygon.call_args[0] == (
        [(0, 0), (0, 10), (10, 10), (10, 0)],
    )

    assert m_ax.add_patch.call_count == 1
    assert m_ax.add_patch.call_args == ((m_plt.Polygon.return_value,), {})
    assert m_ax.scatter.call_count == 1
    assert m_ax.scatter.call_args[0] == ((42, 666), (666, 42))

    assert m_ax.axis.call_count == 1
    assert m_ax.axis.call_args == (((0, 666, 0, 666),),)

    assert m_plt.savefig.call_count == 1
    assert m_plt.savefig.call_args == ((expected,), {'filetype': 'png'})


if __name__ == '__main__':
    pytest.main(__file__)
