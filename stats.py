import csv
import os
import pickle
import pstats


def gather_stats(data_dir):
    stats_filename = os.path.join(data_dir, 'stats.csv')
    with open(stats_filename, 'w') as f:
        fieldnames = [
            'problem', 'edges', 'weight', 'running_time',
            'function_calls', 'primitive_calls']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for filename in sorted(os.listdir(data_dir)):
            if filename.endswith('.profile'):
                pickle_filename = filename[:-8] + '.pickle'
                with open(os.path.join(data_dir, pickle_filename), 'rb') as fp:
                    solution = pickle.load(fp)
                stats = pstats.Stats(os.path.join(data_dir, filename))
                writer.writerow({
                    fieldnames[0]: filename[:-8],
                    fieldnames[1]: len(solution),
                    fieldnames[2]: solution.weight,
                    fieldnames[3]: stats.total_tt,
                    fieldnames[4]: stats.total_calls,
                    fieldnames[5]: stats.prim_calls,
                })
