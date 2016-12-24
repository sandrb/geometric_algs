#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.cli` module.

"""
import pytest

from spanners import cli


@pytest.mark.parametrize('flag', ['-V', '--version'])
def test_main_version(capsys, mocker, flag):
    """
    Test for `cli.main` which tests the version number.

    Args:
        flag (str)

    """
    version = '123.456.789'
    mocker.patch('spanners.__version__', new=version)
    mocker.patch('spanners.cli.sys.argv', ['exec', flag])

    with pytest.raises(SystemExit):
        cli.main()
    assert capsys.readouterr()[0] == version + '\n'


@pytest.mark.parametrize('seed, poly', [
    (None, None), (666, None), (666, 42), (None, 42),
])
def test_main_generate(mocker, seed, poly):
    """
    Test for `cli.main` which tests the generate command.

    Args:
        seed (int): The seed to use.
        poly (int): The polygonizer to use.

    """
    m_generate = mocker.patch('spanners.cli.service.generate')

    argv = 'exec generate 1000 1000 40 20 file.txt'.split()
    if seed is not None:
        argv.append('-s')
        argv.append(seed)
    if poly is not None:
        argv.append('-p')
        argv.append(poly)
    mocker.patch('spanners.cli.sys.argv', argv)

    output = cli.main()
    assert output is None

    assert m_generate.call_count == 1
    assert m_generate.call_args[0] == (1000, 1000, 40, 20)
    assert m_generate.call_args[1] == {
        'seed': seed,
        'filename': 'file.txt',
        'polygonizer': poly,
    }


@pytest.mark.parametrize('argv', [
    'exec generate x 1000 40 20 file.txt',
    'exec generate 1000 y 40 20 file.txt',
    'exec generate 1000 1000 n 20 file.txt',
    'exec generate 1000 1000 40 m file.txt',
    'exec generate 1000 1000 40 m file.txt --seed seed',
    'exec generate 1000 1000 40 m file.txt --polygonizer poly',
])
def test_main_generate_value_error(mocker, argv):
    """
    Test for `cli.main` which tests the generate command.

    Args:
        argv (str): The command used on the cli.

    """
    m_generate = mocker.patch('spanners.cli.service.generate')
    mocker.patch('spanners.cli.sys.argv', argv.split())

    with pytest.raises(ValueError):
        cli.main()

    assert m_generate.call_count == 0


def test_main_visualize(mocker):
    """
    Test for `cli.main` which tests the visualize command.

    """
    m_visualize = mocker.patch('spanners.cli.service.visualize')

    argv = 'exec visualize in.txt out.png'.split()
    mocker.patch('spanners.cli.sys.argv', argv)

    output = cli.main()
    assert output is None

    assert m_visualize.call_count == 1
    assert m_visualize.call_args[0] == ('in.txt', 'out.png')


if __name__ == '__main__':
    pytest.main(__file__)
