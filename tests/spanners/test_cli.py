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


@pytest.mark.parametrize('argv, algorithm, file_out', [
    ('exec solve in.txt', None, None),
    ('exec solve -a greedy in.txt', 'greedy', None),
    ('exec solve -a wspd in.txt', 'wspd', None),
    ('exec solve in.txt out.pickle', None, 'out.pickle'),
    ('exec solve -a greedy in.txt out.pickle', 'greedy', 'out.pickle'),
    ('exec solve -a wspd in.txt out.pickle', 'wspd', 'out.pickle'),
])
def test_main_solve(mocker, argv, algorithm, file_out):
    """
    Test for `cli.main` which tests the 'solve' command.

    Args:
        argv (str): The command used on the cli.
        algorithm (str): The algorithm expected to be used.
        file_out (str): The name of the output file.


    """
    m_solve = mocker.patch('spanners.cli.service.solve')
    output = _patch_argv_and_call_main(mocker, argv.split())
    assert output is None

    assert m_solve.call_count == 1
    assert m_solve.call_args == (('in.txt', algorithm, file_out),)


@pytest.mark.parametrize('file_out', [
    None,
    'out.png',
])
def test_main_render_problem(mocker, file_out):
    """
    Test for `cli.main` which tests the 'render problem' command.

    Args:
        file_out (str): The name of the output file.

    """
    m_render = mocker.patch('spanners.cli.service.render_problem')

    argv = 'exec render problem in.txt'.split()
    if file_out:
        argv.append(file_out)

    output = _patch_argv_and_call_main(mocker, argv)
    assert output is None

    assert m_render.call_count == 1
    assert m_render.call_args[0] == ('in.txt', file_out)


@pytest.mark.parametrize('argv, algorithm, compute, file_out', [
    ('exec render solution in.txt', None, False, None),
    ('exec render solution -a greedy in.txt', 'greedy', False, None),
    ('exec render solution -a wspd in.txt', 'wspd', False, None),
    ('exec render solution in.txt out.png', None, False, 'out.png'),
    ('exec render solution -a greedy in.txt out.png', 'greedy', False,
     'out.png'),
    ('exec render solution -a wspd in.txt out.png', 'wspd', False, 'out.png'),
    ('exec render solution -c in.txt', None, True, None),
    ('exec render solution -a greedy -c in.txt', 'greedy', True, None),
    ('exec render solution -a wspd -c in.txt', 'wspd', True, None),
    ('exec render solution -c in.txt out.png', None, True, 'out.png'),
    ('exec render solution -a greedy -c in.txt out.png', 'greedy', True,
     'out.png'),
    ('exec render solution -a wspd -c in.txt out.png', 'wspd', True,
     'out.png'),
])
def test_main_render_solution(mocker, argv, algorithm, compute, file_out):
    """
    Test for `cli.main` which tests the 'render solution' command.

    Args:
        argv (str): The command used on the cli.
        algorithm (str): The algorithm expected to be used.
        compute (bool): Whether the solution should be computed.
        file_out (str): The name of the output file.

    """
    m_render = mocker.patch('spanners.cli.service.render_solution')

    output = _patch_argv_and_call_main(mocker, argv.split())
    assert output is None

    assert m_render.call_count == 1
    assert m_render.call_args[0] == ('in.txt', algorithm, compute, file_out)


def test_main_show_problem(mocker):
    """
    Test for `cli.main` which tests the 'show problem' command.

    """
    m_show = mocker.patch('spanners.cli.service.show_problem')

    argv = 'exec show problem in.txt'.split()

    output = _patch_argv_and_call_main(mocker, argv)
    assert output is None

    assert m_show.call_count == 1
    assert m_show.call_args[0] == ('in.txt',)


@pytest.mark.parametrize('argv, algorithm, compute', [
    ('exec show solution in.txt', None, False),
    ('exec show solution -a greedy in.txt', 'greedy', False),
    ('exec show solution -a wspd in.txt', 'wspd', False),
    ('exec show solution -c in.txt', None, True),
    ('exec show solution -a greedy -c in.txt', 'greedy', True),
    ('exec show solution -a wspd -c in.txt', 'wspd', True),
])
def test_main_show_solution(mocker, argv, algorithm, compute):
    """
    Test for `cli.main` which tests the 'show solution' command.

    Args:
        argv (str): The command used on the cli.
        algorithm (str): The algorithm expected to be used.
        compute (bool): Whether the solution should be computed.

    """
    m_show = mocker.patch('spanners.cli.service.show_solution')

    output = _patch_argv_and_call_main(mocker, argv.split())
    assert output is None

    assert m_show.call_count == 1
    assert m_show.call_args[0] == ('in.txt', algorithm, compute)


def _patch_argv_and_call_main(mocker, argv):
    mocker.patch('spanners.cli.sys.argv', argv)
    output = cli.main()
    return output


if __name__ == '__main__':
    pytest.main(__file__)
