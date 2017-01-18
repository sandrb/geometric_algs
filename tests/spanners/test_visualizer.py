#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.visualizer` module.

"""
import matplotlib.pyplot as plt
import pytest

from spanners import visualizer


@pytest.fixture
def m_collections(mocker):
    """
    Provide a mock for `matplotlib.collections`.

    Returns:
        MagicMock: A mock for `matplotlib.collections`.

    """
    return mocker.patch('spanners.visualizer.matplotlib.collections')


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


def test_render_problem(m_plt, problem):
    """
    Test for `visualizer.render_problem`.

    Args:
        m_plt (MagicMock): A mock for `matplotlib.pyplot`.
        problem (models.Problem): The problem to test.

    """
    filename = 'image.png'
    output = visualizer.render_problem(problem, filename)
    assert output is None

    m_fig, m_ax = m_plt.subplots.return_value

    assert m_fig.call_count == 0
    assert _is_problem_plotted(m_plt, m_ax)
    assert _is_axis_configured(m_ax)

    assert m_plt.savefig.call_count == 1
    assert m_plt.savefig.call_args == ((filename,),)


def test_show_problem(m_plt, problem):
    """
    Test for `visualizer.show_problem`.

    Args:
        m_plt (MagicMock): A mock for `matplotlib.pyplot`.
        problem (models.Problem): The problem to test.

    """
    output = visualizer.show_problem(problem)
    assert output is None

    m_fig, m_ax = m_plt.subplots.return_value

    assert m_fig.call_count == 0
    assert _is_problem_plotted(m_plt, m_ax)
    assert _is_axis_configured(m_ax)

    assert m_plt.show.call_count == 1
    assert m_plt.show.call_args == ()


def test_render_solution(m_plt, m_collections, solution):
    """
    Test for `visualizer.render_solution`.

    Args:
        m_plt (MagicMock): A mock for `matplotlib.pyplot`.
        m_collections (MagicMock): A mock for `matplotlib.collections`.
        solution (models.Solution): The solution to test.

    """
    filename = 'image.png'
    output = visualizer.render_solution(solution, filename)
    assert output is None

    m_fig, m_ax = m_plt.subplots.return_value

    assert m_fig.call_count == 0
    assert _is_problem_plotted(m_plt, m_ax)
    assert _is_solution_plotted(m_collections, m_ax)
    assert _is_axis_configured(m_ax)

    assert m_plt.savefig.call_count == 1
    assert m_plt.savefig.call_args == ((filename,),)


def test_show_solution(m_plt, m_collections, solution):
    """
    Test for `visualizer.show_solution`.

    Args:
        m_plt (MagicMock): A mock for `matplotlib.pyplot`.
        m_collections (MagicMock): A mock for `matplotlib.collections`.
        solution (models.Solution): The solution to test.

    """
    output = visualizer.show_solution(solution)
    assert output is None

    m_fig, m_ax = m_plt.subplots.return_value

    assert m_fig.call_count == 0
    assert _is_problem_plotted(m_plt, m_ax)
    assert _is_solution_plotted(m_collections, m_ax)
    assert _is_axis_configured(m_ax)

    assert m_plt.show.call_count == 1
    assert m_plt.show.call_args == ()


def _is_problem_plotted(m_plt, m_ax):
    __tracebackhide__ = True

    assert m_plt.Polygon.call_count == 1
    assert m_plt.Polygon.call_args[0] == (
        [(0, 0), (0, 10), (10, 10), (10, 0)],
    )

    assert m_ax.add_patch.call_count == 1
    assert m_ax.add_patch.call_args == ((m_plt.Polygon.return_value,), {})
    assert m_ax.scatter.call_count == 1
    assert m_ax.scatter.call_args[0] == ((42, 666), (666, 42))

    return True


def _is_solution_plotted(m_collections, m_ax):
    # __tracebackhide__ = True

    print(m_ax.mock_calls)

    m_line_collection = m_collections.LineCollection

    p = (42, 666)
    q = (666, 42)
    assert m_line_collection.call_count == 1
    assert len(m_line_collection.call_args[0]) == 1
    assert m_line_collection.call_args[0][0] in {((p, q),), ((q, p),)}

    assert m_ax.add_collection.call_count == 1
    assert m_ax.add_collection.call_args == (
        (m_line_collection.return_value, ),
        {},
    )

    return True


def _is_axis_configured(m_ax):
    __tracebackhide__ = True

    assert m_ax.axis.call_count == 1
    assert m_ax.axis.call_args == (((0, 666, 0, 666),),)

    return True


if __name__ == '__main__':
    pytest.main(__file__)
