#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.visualizer` module.

"""
import pytest

from spanners import service


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


@pytest.mark.parametrize(
    'challenge_filename, image_filename, filetype, expected', [
        ('challenge.txt', None, None, 'challenge'),
        ('challenge.txt', None, 'png', 'challenge'),
        ('challenge.txt', 'image.png', None, 'image.png'),
        ('challenge.txt', 'image.png', 'png', 'image.png'),
        ('challenge.file', None, None, 'challenge.file'),
    ])
def test_visualize(
        mocker, challenge_filename, image_filename, filetype, expected):
    """
    Test for `service.visualize`.

    Args:
        challenge_filename (str): The filename of the data challenge
            file for which to visualize the problem.
        image_filename (str): The filename to use for the image of the
            problem.
        filetype (str): The filetype of the image.
        expected (str): The expected image filename.

    """
    m_open = mocker.mock_open()
    mocker.patch('spanners.service.open', m_open)
    m_challenge = mocker.patch('spanners.service.challenge.load')
    m_visualize = mocker.patch('spanners.service.visualizer.vizualize_problem')

    output = service.visualize(challenge_filename, image_filename, filetype)
    assert output is None

    assert m_open.call_count == 1
    assert m_open.call_args == ((challenge_filename,),)

    assert m_challenge.call_count == 1
    assert m_challenge.call_args == ((m_open.return_value,),)

    assert m_visualize.call_count == 1
    m_problem = m_challenge.return_value
    assert m_visualize.call_args[0] == (m_problem, expected, filetype)


if __name__ == '__main__':
    pytest.main(__file__)
