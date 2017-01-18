#!/usr/bin/env python3.6
"""
This module holds tests for the `spanners.challenge` module.

"""
import pytest

from spanners import challenge


@pytest.fixture
def file_content():
    """
    Provide the file contents of a data challenge file.

    Returns:
        List[str]: A list of lines in the data challenge file.

    """
    return [
        '2',
        '4',
        '314 271',
        '42 666',
        '666 42',
        '0 0',
        '0 10',
        '10 10',
        '10 0',
    ]


def test_load(mocker, file_content, problem):
    """
    Test for `challenge.load`.

    Args:
        file_content (List[str]): Data to be read from a file.
        problem (models.Problem): The expected problem to be loaded.

    """
    m_fs = mocker.mock_open(read_data='\n'.join(file_content))
    output = challenge.load(m_fs('input.txt'))
    assert type(output) == type(problem)
    assert dict(output) == dict(problem)


def test_load_type_error(mocker, file_content):
    """
    Test for `challenge.load` where there is too few point data.

    Args:
        file_content (List[str]): Data to be read from a file.

    """
    with pytest.raises(challenge.FileFormatError) as ctx:
        m_fs = mocker.mock_open(read_data='\n'.join(file_content[:-1]))
        challenge.load(m_fs('input.txt'))
    assert type(ctx.value.__cause__) == TypeError


def test_load_value_error(mocker, file_content):
    """
    Test for `challenge.load` where the point data contains a string.

    Args:
        file_content (List[str]): Data to be read from a file.

    """
    file_content[-1] = 'aaa bbb'
    with pytest.raises(challenge.FileFormatError) as ctx:
        m_fs = mocker.mock_open(read_data='\n'.join(file_content))
        challenge.load(m_fs('input.txt'))
    assert type(ctx.value.__cause__) == ValueError


def test_load_file_format_error(mocker, file_content):
    """
    Test for `challenge.load` where there is too much point data.

    Args:
        file_content (List[str]): Data to be read from a file.

    """
    file_content.append('99999 99999')
    with pytest.raises(challenge.FileFormatError):
        m_fs = mocker.mock_open(read_data='\n'.join(file_content))
        challenge.load(m_fs('input.txt'))


def test_dump(mocker, problem, file_content):
    """
    Test for `challenge.dump`.

    Args:
        problem (models.Problem): The problem to test.
        file_content (List[str]): The data expected to be dumped.

    """
    m_fs = mocker.MagicMock()
    output = challenge.dump(problem, m_fs)
    assert output is None

    assert m_fs.write.call_count == 1
    assert m_fs.write.call_args == (('\n'.join(file_content) + '\n',),)


if __name__ == '__main__':
    pytest.main(__file__)
