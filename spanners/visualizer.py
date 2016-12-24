"""
This module is for vizualizing problems.

"""
import matplotlib.pyplot as plt


def vizualize_problem(problem, filename, filetype=None):
    """
    Visualize a problem by generating an image.

    Args:
        problem (models.Problem): The problem to visualize.
        filename (str): The filename to use for the image of the
            problem.

    Keyword Args:
        filetype (str): The filetype of the image.

    """
    if not filetype:
        filetype = 'png'

    suffix = '.{}'.format(filetype)
    if not filename.lower().endswith(suffix):
        filename += suffix

    fig, ax = plt.subplots()

    obstacle = plt.Polygon(
        problem.obstacle, closed=True, color='blue', alpha=0.5)
    ax.add_patch(obstacle)
    ax.scatter(*zip(*problem.points), marker='o', color='red')

    x_min = min(point.x for point in problem)
    x_max = max(point.x for point in problem)
    y_min = min(point.y for point in problem)
    y_max = max(point.y for point in problem)

    ax.axis((x_min, x_max, y_min, y_max))

    plt.savefig(filename, filetype=filetype)
