"""
This module is for visualizing problems.

"""
import matplotlib.collections
import matplotlib.pyplot as plt


def render_problem(problem, filename):
    """
    Render an image of the problem.

    Args:
        problem (models.Problem): The problem for which to render an
            image.
        filename (str): The filename to use for the image of the
            problem.

    """
    _plot_data(problem)
    plt.savefig(filename)


def show_problem(problem):
    """
    Show a screen with a graph corresponding to the problem.

    Args:
        problem (models.Problem): The problem for which to show a
            screen with a graph corresponding to the problem.

    """
    _plot_data(problem)
    plt.show()


def render_solution(solution, filename):
    """
    Render an image of the solution.

    Args:
        solution (models.Solution): The solution for which to render an
            image.
        filename (str): The filename to use for the image of the
            solution.

    """
    _plot_data(solution.problem, solution)
    plt.savefig(filename)


def show_solution(solution):
    """
    Show a screen with a graph corresponding to the solution.

    Args:
        solution (models.Solution): The solution for which to show a
            screen with a graph corresponding to the solution.

    """
    _plot_data(solution.problem, solution)
    plt.show()


def _plot_data(problem, solution=None):
    fig, ax = plt.subplots()
    _plot_problem(problem, ax)
    if solution is not None:
        _plot_solution(solution, ax)
    _configure_axis(problem, ax)


def _plot_problem(problem, ax):
    obstacle = plt.Polygon(
        problem.obstacle, closed=True, color='blue', alpha=0.5)
    ax.add_patch(obstacle)
    ax.scatter(*zip(*problem.points), marker='o', color='red')


def _plot_solution(solution, ax):
    """
    Plot the solution data.

    Args:
        solution (models.Solution): The solutino for which to plot the
            data.
        ax (matplotlib.axis.Axes): The `Axes` on which to plot the data.

    Todo:
        Issue with NumPy?

        Cannot use `models.Edge` directly:

        >>> import matplotlib.collections
        >>>
        >>> from spanners import generator
        >>> from spanners import calculator
        >>>
        >>>
        >>> problem = generator.generate(1000, 1000, 2, 4)
        >>> solution = calculator.compute_greedy_spanner(problem)
        >>>
        >>> line_segments = matplotlib.collections.LineCollection(
        ...     solution, colors=['green'])
        Traceback (most recent call last):
           ...
        TypeError: float() argument must be a string or a number, not 'Edge'

        The function `numpy.asarray` does not deal correctly with sets:

        >>> import numpy
        >>> numpy.asarray((), numpy.float_)
        array([], dtype=float64)
        >>> numpy.asarray([], numpy.float_)
        array([], dtype=float64)
        >>> numpy.asarray(set(), numpy.float_)
        Traceback (most recent call last):
           ...
        TypeError: float() argument must be a string or a number, not 'set'

    """
    segments = tuple((p, q) for p, q in solution)
    line_segments = matplotlib.collections.LineCollection(
        segments, colors=['green'])
    ax.add_collection(line_segments)


def _configure_axis(problem, ax):
    x_min = min(point.x for point in problem)
    x_max = max(point.x for point in problem)
    y_min = min(point.y for point in problem)
    y_max = max(point.y for point in problem)

    ax.axis((x_min, x_max, y_min, y_max))


__test__ = {'error': _plot_solution}
