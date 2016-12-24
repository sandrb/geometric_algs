"""
This module holds the services.

"""
from spanners import challenge
from spanners import generator
from spanners import visualizer


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


def visualize(challenge_filename, image_filename=None, filetype=None):
    """
    Visualize the problem from a data challenge file.

    It generates an image of the problem at the specified location.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to visualize the problem.

    Keyword Args:
        image_filename (str): The filename to use for the image of the
            problem. Defaults to `challenge_filename`. A '.txt' suffix
            is ignored.
        filetype (str): The filetype of the image.

    """
    if not image_filename:
        image_filename = challenge_filename
        if image_filename.lower().endswith('.txt'):
            image_filename = image_filename[:-4]

    with open(challenge_filename) as f:
        problem = challenge.load(f)

    visualizer.vizualize_problem(problem, image_filename, filetype)
