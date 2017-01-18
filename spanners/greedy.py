"""
This module is for calculating the spanner trees greedily.

"""
import itertools

import pyvisgraph as vg

from spanners import models


def compute_spanner(problem):
    """
    Compute a t-spanner in a greedy manner.

    Args:
        problem (Problem): The problem for which to compute the
            t-spanner, where t is based on the ratio of the problem.

    """
    points = _convert_to_vg_points(problem.points)
    obstacle = _convert_to_vg_points(problem.obstacle)

    visibility_graph = _create_visibility_graph(points, obstacle)

    pairs = itertools.combinations(points, 2)
    paths = {}
    distances = {}
    for p, q in pairs:
        pair = frozenset((p, q))

        shortest_path = visibility_graph.shortest_path(p, q)
        distance = _calculate_path_length(shortest_path)

        paths[pair] = shortest_path
        distances[pair] = distance

    spanner = _create_spanner(paths, distances, problem.ratio)
    return _create_solution(problem, visibility_graph, spanner)


def _convert_to_vg_points(points):
    return [vg.Point(*p) for p in points]


def _create_visibility_graph(points, obstacle):
    visibility_graph = vg.VisGraph()
    visibility_graph.build([obstacle] + [[point] for point in points])
    """
    Only the obstacle will be in the dictionary of polygons,
    assuming that the obstacle consists of at least three points.

    One might expect to use the following two lines:

    >>> visibility_graph.build([obstacle])
    >>> visibility_graph.update(points)

    However, update does not take care of visibility amongst the points
    themselves.

    """
    return visibility_graph


def _create_spanner(paths, distances, ratio):
    pairs = sorted(distances, key=distances.__getitem__)
    spanner = vg.Graph([])

    for pair in pairs:
        p, q = pair
        try:
            path = vg.shortest_path.shortest_path(spanner, p, q)
        except KeyError:
            distance = -1
        else:
            distance = _calculate_path_length(path)

        shortest_distance = distances[pair]

        if distance == -1 or distance > ratio * shortest_distance:
            shortest_path = paths[pair]
            _add_path(spanner, shortest_path)
        else:
            # print(pair)  # TODO: Why are there pairs for 1-spanner?
            pass
    return spanner


def _calculate_path_length(path):
    distance = vg.visible_vertices.edge_distance
    return sum(distance(p, q) for p, q in zip(path, path[1:]))


def _add_path(spanner, path):
    for p, q in zip(path, path[1:]):
        spanner.add_edge(vg.Edge(p, q))


def _create_solution(problem, visibility_graph, spanner):
    all_edges = visibility_graph.visgraph.get_edges()
    max_edges = len(all_edges)
    max_weight = _calculate_length(all_edges)
    edges = {_convert_to_edge(edge) for edge in spanner.get_edges()}
    solution = models.Solution(problem, max_edges, max_weight, edges)
    return solution


def _calculate_length(edges):
    distance = vg.visible_vertices.edge_distance
    return sum(distance(edge.p1, edge.p2) for edge in edges)


def _convert_to_edge(edge):
    return models.Edge(_convert_to_point(edge.p1), _convert_to_point(edge.p2))


def _convert_to_point(point):
    return models.Point(int(point.x), int(point.y))
