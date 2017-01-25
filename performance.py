"""
This module contains everything related to performancee testing.

"""
import cProfile
import os

from spanners import service


random_data_dir = 'random_data_sets'
challenge_data_dir = 'spanner_data_sets'


def random_data(x=10000, y=10000, seed=42):
    os.makedirs(random_data_dir, exist_ok=True)
    for m in _powers_of_two():
        for n in _powers_of_two():
            filename = os.path.join(
                random_data_dir, '{}x{}_n-{}_m-{}_seed-{}.txt'.format(
                    x, y, n, m, seed))
            service.generate(x, y, n, m, seed, filename)


def _powers_of_two(start=2, end=10):
    yield from (2 ** i for i in range(start, end))


def random_greedy():
    _solve('greedy', random_data_dir)


def random_wspd():
    _solve('wspd', random_data_dir)


def challenge_greedy():
    _solve('greedy', challenge_data_dir)


def challenge_wspd():
    _solve('wspd', challenge_data_dir)


def _solve(algorithm, data_dir):
    os.makedirs(os.path.join(data_dir, algorithm), exist_ok=True)
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            challenge_filename = os.path.join(data_dir, filename)
            output_filename = os.path.join(data_dir, algorithm, filename[:-4])
            pickle_filename = output_filename + '.pickle'
            profile_filename = output_filename + '.profile'
            cmd = 'service.solve(' \
                'challenge_filename, algorithm, pickle_filename)'
            cProfile.runctx(cmd, globals(), locals(), profile_filename)
