#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.service` module.

"""
import pytest

from spanners import service


@pytest.fixture
def m_open(mocker):
    """
    Provide a `mock_open` mock.

    Returns:
        MagicMock: A `mock_open` mock.

    """
    m_open = mocker.mock_open()
    mocker.patch('spanners.service.open', m_open)
    return m_open


@pytest.mark.parametrize('filename, seed, expected', [
    ('challenge.txt', None, 'challenge.txt'),
    ('challenge.txt', 666, 'challenge.txt'),
    (None, None, '1000x1000 40-points 20-obstacle.txt'),
    (None, 666, '1000x1000 40-points 20-obstacle seed 666.txt'),
])
def test_generate(mocker, filename, seed, expected):
    """
    Test for `service.generate`.

    Args:
        filename (str): The filename to use for the data challenge
            file.
        seed (int): The seed to use.
        expected (str): The expected filename to be used.

    """
    m_open = mocker.mock_open()
    mocker.patch('spanners.service.open', m_open)
    m_generate = mocker.patch('spanners.service.generator.generate')
    m_dump = mocker.patch('spanners.service.challenge.dump')

    output = service.generate(1000, 1000, 40, 20, seed, filename, 2)
    assert output is None

    assert m_open.call_count == 1
    assert m_open.call_args == ((expected, 'w'),)

    assert m_generate.call_count == 1
    assert m_generate.call_args == ((1000, 1000, 40, 20, seed, 2), {})

    m_problem = m_generate.return_value
    assert m_dump.call_count == 1
    assert m_dump.call_args == ((m_problem, m_open.return_value), {})


@pytest.mark.parametrize('challenge_filename, image_filename, expected', [
    ('challenge.txt', None, 'challenge.png'),
    ('challenge.txt', 'image.png', 'image.png'),
    ('challenge.file', None, 'challenge.file.png'),
])
def test_render_problem(
        mocker, m_open, challenge_filename, image_filename, expected):
    """
    Test for `service.render_problem`.

    Args:
        m_open (MagicMock): A `mock_open` mock.
        challenge_filename (str): The filename of the data challenge
            file for which to render an image the problem.
        image_filename (str): The filename to use for the image of the
            problem.
        expected (str): The expected image filename.

    """
    m_challenge = mocker.patch('spanners.service.challenge.load')
    m_render_problem = mocker.patch(
        'spanners.service.visualizer.render_problem')

    output = service.render_problem(challenge_filename, image_filename)
    assert output is None

    assert _is_challenge_loaded(m_open, m_challenge, challenge_filename)

    assert m_render_problem.call_count == 1
    m_problem = m_challenge.return_value
    assert m_render_problem.call_args == ((m_problem, expected),)


def test_show_problem(mocker, m_open):
    """
    Test for `service.show_problem`.

    Args:
        m_open (MagicMock): A `mock_open` mock.

    """
    challenge_filename = 'challenge.txt'
    m_challenge = mocker.patch('spanners.service.challenge.load')
    m_show_problem = mocker.patch('spanners.service.visualizer.show_problem')

    output = service.show_problem(challenge_filename)
    assert output is None

    assert _is_challenge_loaded(m_open, m_challenge, challenge_filename)

    assert m_show_problem.call_count == 1
    m_problem = m_challenge.return_value
    assert m_show_problem.call_args == ((m_problem,),)


@pytest.mark.parametrize(
    'challenge_filename, algorithm, image_filename, expected', [
        ('challenge.txt', None, None, 'challenge_spanner.png'),
        ('challenge.txt', None, 'image.png', 'image.png'),
        ('challenge.file', None, None, 'challenge.file_spanner.png'),
        ('challenge.txt', 'greedy', None, 'challenge_spanner.png'),
        ('challenge.txt', 'greedy', 'image.png', 'image.png'),
        ('challenge.file', 'greedy', None, 'challenge.file_spanner.png'),
        ('challenge.txt', 'wspd', None, 'challenge_spanner.png'),
        ('challenge.txt', 'wspd', 'image.png', 'image.png'),
        ('challenge.file', 'wspd', None, 'challenge.file_spanner.png'),
    ])
def test_render_solution(
        mocker, m_open, challenge_filename, algorithm, image_filename,
        expected):
    """
    Test for `service.render_solution`.

    Args:
        m_open (MagicMock): A `mock_open` mock.
        challenge_filename (str): The filename of the data challenge
            file for which to render an image the problem.
        algorithm (str): The algorithm to use.
        image_filename (str): The filename to use for the image of the
            problem.
        expected (str): The expected image filename.

    """
    m_challenge = mocker.patch('spanners.service.challenge.load')
    m_greedy = mocker.patch('spanners.service.greedy.compute_spanner')
    m_wspd = mocker.patch('spanners.service.wspd.compute_spanner')
    render_solution = mocker.patch(
        'spanners.service.visualizer.render_solution')

    if algorithm == 'wspd':
        m_compute = m_wspd
        m_not_compute = m_greedy
    else:
        m_compute = m_greedy
        m_not_compute = m_wspd

    output = service.render_solution(
        challenge_filename, algorithm, image_filename)
    assert output is None

    assert _is_challenge_loaded(m_open, m_challenge, challenge_filename)
    assert _is_solution_computed(m_compute, m_challenge.return_value)
    assert not m_not_compute.called

    assert render_solution.call_count == 1
    m_problem = m_compute.return_value
    assert render_solution.call_args == ((m_problem, expected),)


@pytest.mark.parametrize('algorithm', [
    None,
    'greedy',
    'wspd',
])
def test_show_solution(mocker, m_open, algorithm):
    """
    Test for `service.show_solution`.

    Args:
        m_open (MagicMock): A `mock_open` mock.
        algorithm (str): The algorithm to use.

    """
    challenge_filename = 'challenge.txt'
    m_challenge = mocker.patch('spanners.service.challenge.load')
    m_greedy = mocker.patch('spanners.service.greedy.compute_spanner')
    m_wspd = mocker.patch('spanners.service.wspd.compute_spanner')
    m_show_solution = mocker.patch('spanners.service.visualizer.show_solution')

    if algorithm == 'wspd':
        m_compute = m_wspd
        m_not_compute = m_greedy
    else:
        m_compute = m_greedy
        m_not_compute = m_wspd

    output = service.show_solution(challenge_filename, algorithm)
    assert output is None

    assert _is_challenge_loaded(m_open, m_challenge, challenge_filename)
    assert _is_solution_computed(m_compute, m_challenge.return_value)
    assert not m_not_compute.called

    assert m_show_solution.call_count == 1
    m_problem = m_compute.return_value
    assert m_show_solution.call_args == ((m_problem,),)


def _is_challenge_loaded(m_open, m_challenge, challenge_filename):
    __tracebackhide__ = True

    assert m_open.call_count == 1
    assert m_open.call_args == ((challenge_filename,),)

    assert m_challenge.call_count == 1
    assert m_challenge.call_args == ((m_open.return_value,),)

    return True


def _is_solution_computed(m_compute, m_problem):
    __tracebackhide__ = True

    assert m_compute.call_count == 1
    assert m_compute.call_args == ((m_problem,),)

    return True


if __name__ == '__main__':
    pytest.main(__file__)
