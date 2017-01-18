"""
This module holds the services.

"""
from spanners import challenge
from spanners import generator
from spanners import greedy
from spanners import visualizer
from spanners import wspd


def generate(max_x, max_y, n, m, seed=None, filename=None, polygonizer=None):
    """
    Generate a problem and store it in a data challenge file.

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
        filename (str): The filename to use for the data challenge
            file. Defaults to
            `'{x}x{y} {n}-points {m}-obstacle (seed {seed})?.txt'`
        polygonizer (int): The polygonizer to use. Either `1` or `2`.
            Defaults to `2`.

    Raises:
        ValueError: If one of the arguments is not positive or if an
            invalid polygonizer is specified..

    """
    if not filename:
        filename = '{x}x{y} {n}-points {m}-obstacle{seed}.txt'.format(
            x=max_x, y=max_y, n=n, m=m,
            seed=' seed {}'.format(seed) if seed else '')

    problem = generator.generate(max_x, max_y, n, m, seed, polygonizer)
    with open(filename, 'w') as f:
        challenge.dump(problem, f)


def render_problem(challenge_filename, image_filename=None):
    """
    Render an image from a data challenge file.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to render an image of the problem.

    Keyword Args:
        image_filename (str): The filename to use for the image of the
            problem. Defaults to '`challenge_filename`.png'. A '.txt'
            suffix in the data challenge filename is ignored.

    """
    if not image_filename:
        image_filename = _extract_base_filename(challenge_filename)
        image_filename += '.png'

    problem = _load_challenge(challenge_filename)
    visualizer.render_problem(problem, image_filename)


def show_problem(challenge_filename):
    """
    Show the graph corresponding to the data challenge file.

    This opens a separate screen.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to show a graph corresponding to the
            problem.

    """
    problem = _load_challenge(challenge_filename)
    visualizer.show_problem(problem)


def render_solution(challenge_filename, algorithm=None, image_filename=None):
    """
    Render an image of a solution to a data challenge.

    The solution will be computed on the fly and may take some time.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to render an image of a solution of the
            problem.

    Keyword Args:
        algorithm (str): The algorithm to use for computing the
            solution. Defaults to `greedy` if `None`.
        image_filename (str): The filename to use for the image of the
            problem. Defaults to '`challenge_filename`_spanner.png'.
            A '.txt' suffix in the data challenge filename is ignored.

    """
    if not image_filename:
        image_filename = _extract_base_filename(challenge_filename)
        image_filename += '_spanner.png'

    solution = _compute_solution(challenge_filename, algorithm)
    visualizer.render_solution(solution, image_filename)


def show_solution(challenge_filename, algorithm=None):
    """
    Show the spanner corresponding to a solution of a data challenge.

    This opens a separate screen. It may take some time for the screen
    to appear, since the solution will be computed on the fly.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to show a spanner corresponding to a
            solution of the problem.

    Keyword Args:
        algorithm (str): The algorithm to use for computing the
            solution. Defaults to `greedy` if `None`.

    """
    solution = _compute_solution(challenge_filename, algorithm)
    visualizer.show_solution(solution)


def _extract_base_filename(challenge_filename):
    image_filename = challenge_filename
    if image_filename.lower().endswith('.txt'):
        image_filename = image_filename[:-4]
    return image_filename


def _compute_solution(challenge_filename, algorithm):
    problem = _load_challenge(challenge_filename)
    if algorithm == 'wspd':
        solution = wspd.compute_spanner(problem)
    else:
        solution = greedy.compute_spanner(problem)
    return solution


def _load_challenge(challenge_filename):
    with open(challenge_filename) as f:
        problem = challenge.load(f)
    return problem
