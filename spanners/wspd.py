"""
This module is for calculating the spanner trees using wspds.

"""
import pyvisgraph as vg

from spanners import models
from spanners import quadtrees


class Wspd:
    """
    This class is for computing well separated pair decompositions.

    One can inherit from this class and override methods to change the
    behaviour of the algorithm.

    """
    def __init__(self, s=2):
        """
        Initialize a `Wspd`.

        Keyword Args:
            s (int): The separation ratio.

        """
        self.s = s

    def representative(self, quadtree):
        """
        Get the representative of a quadtree.

        Returns:
            models.Point: The representative of the quadtree.

        """
        return next(iter(quadtree), None)

    def pairs(self, u, v=None):
        """
        Compute the well separated pairs.

        Args:
            u (quadtrees.Quadtree): The quadtree containing points for
                which to compute the well separated pair decomposition.

        Keyword Args:
            v (quadtrees.Quadtree): The quadtree containing points for
                which to compute the well separated pair decomposition.
                Defaults to `u`.

        Returns:
            Set[FrozenSet[quadtrees.Quadtree, quadtrees.Quadtree]]:
                A set of well separated quadtree nodes.

        Note:
            Uses recursion.

        """
        if v is None:
            v = u
        if not self.representative(u) or not self.representative(v):
            pairs = set()
        elif self.is_well_separated(u, v):
            pairs = set()
            if u is not v:
                pairs = {frozenset((u, v))}
        else:
            if u.level > v.level:
                u, v = v, u
            children = (u.ne, u.nw, u.sw, u.se)
            pairs = set().union(
                *(self.pairs(child, v) for child in children if child))
        return pairs

    def is_well_separated(self, u, v):
        """
        Chech whether two quadtrees are well separated.

        Args:
            u (quadtrees.Quadtree): The first quadtree.
            v (quadtrees.Quadtree): The second quadtree.

        Returns:
            bool: Whether the two quadtrees are well separated.

        """
        radius_u = u.bounding_box.edge.length / 2 if not u.point else 0
        radius_v = v.bounding_box.edge.length / 2 if not v.point else 0
        center_u = u.bounding_box.center if not u.point else u.point
        center_v = v.bounding_box.center if not v.point else v.point
        radius = max(radius_u, radius_v)
        edge = models.Edge(center_u, center_v)
        return edge.length - 2 * radius > self.s * radius

    def __repr__(self):
        """
        Get the string representation of the wspd algorithm.

        Retuns:
            str: The string representation of the wspd algorithm.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                self.s,
            ])))


class ObstacleWspd(Wspd):
    """
    This class is for computing a wspd with an obstacle.

    """
    def __init__(self, obstacle, s=2):
        """
        Initialize an `ObstacleWspd`.

        Args:
            obstacle (List[models.Point]): The obstacle to avoid.

        Keyword Args:
            s (int): The separation ratio.

        """
        super().__init__(s)
        self.visibility_graph = vg.VisGraph()
        self.visibility_graph.build([[vg.Point(*p) for p in obstacle]])

    def shortest_path(self, u, v):
        """
        Get the shortest path between two quadtrees.

        The shortest path is calculated between the representatives of
        each quadtree.

        Args:
            u (quadtrees.Quadtree): The first quadtree.
            v (quadtrees.Quadtree): The second quadtree.

        Returns:
            List[models.Edge]: List of edges representing the shortest
                path.

        """
        rep_u = self.representative(u)
        rep_v = self.representative(v)
        if rep_u == rep_v:
            path = []
        else:
            vg_path = self.visibility_graph.shortest_path(
                vg.Point(*rep_u), vg.Point(*rep_v))
            path = [
                self._convert_to_edge(p, q)
                for p, q in zip(vg_path, vg_path[1:])]
        return path

    def _convert_to_edge(self, p, q):
        return models.Edge(
            self._convert_to_point(p), self._convert_to_point(q))

    def _convert_to_point(self, point):
        return models.Point(int(point.x), int(point.y))

    def __repr__(self):
        """
        Get the string representation of the obstacle wspd algorithm.

        Retuns:
            str: The string representation of the obstacle wspd
                algorithm.

        """
        return '{classname}({args})'.format(
            classname=type(self).__name__,
            args=', '.join(map(repr, [
                [
                    self._convert_to_point(p)
                    for p in self.visibility_graph.polygons[0]],
                self.s,
            ])))


def compute_spanner(problem):
    """
    Compute a t-spanner using a wspd.

    Args:
        problem (Problem): The problem for which to compute the
            t-spanner, where t is based on the ratio of the problem.

    Returns:
        models.Solution: The solution to the problem.

    """
    s = 4 * (problem.ratio + 1) / (problem.ratio - 1)
    owspd = ObstacleWspd(problem.obstacle, s)
    qt = quadtrees.Quadtree(problem.points)
    pairs = owspd.pairs(qt)
    edges = set(
        edge for u, v in pairs
        for edge in owspd.shortest_path(u, v))
    vg_edges = owspd.visibility_graph.visgraph.get_edges()
    # XXX: max edges is edges in visibility graph of the obstacle.
    max_edges = -1 * len(vg_edges)
    # XXX: max weight is weight of edges in visibility of the obstacle.
    max_weight = -1 * sum(
        vg.visible_vertices.edge_distance(vg_edge.p1, vg_edge.p2)
        for vg_edge in vg_edges)
    solution = models.Solution(problem, max_edges, max_weight, edges)
    return solution
