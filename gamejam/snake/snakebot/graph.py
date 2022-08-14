# option 1. Use dfs to find all paths from each sense to action, ignore those that don't travel. Compute up each path and total on action
# option 2. Use bfs to recursively compute all previous nodes from action that reach back to sense and unravel as feedfoward

from collections import deque
from dataclasses import dataclass
from typing import TypeVar, Union, Tuple
from functools import reduce


T = TypeVar('T')


@dataclass
class Graph:
    N: int
    E: int
    nodes: list
    edges: list
    adj: dict
    indegree: dict
    outdegree: dict
    
    def __repr__(self):
        return f"Graph(N={self.N}, E={self.E})"


def create(edges: list) -> Graph:
    nodes = {e.left for e in edges}.union({e.right for e in edges})
    adj = {}
    indegree = {}
    for edge in edges:
        adj.setdefault(edge.left, []).append(edge)
        indegree[edge.right] = 1 + indegree.get(edge.right, 0)

    outdegree = {node: len(adj[node]) for node in adj}

    return Graph(
        N=len(nodes),
        E=len(edges),
        nodes=nodes,
        edges=edges,
        adj=adj,
        indegree=indegree,
        outdegree=outdegree)


def indegree(g: Graph, v: T) -> int:
    return g.indegree.get(v, 0)


def outdegree(g: Graph, v: T) -> int:
    return len(g.adj[v]) if v in g.adj else 0


def adjacent(g: Graph, v: T) -> list:
    return g.adj.get(v, [])


def neighbors(g: Graph, v: T) -> Union[None, list]:
    return adjacent(g, v)


def edges(g):
    return g.edges


def bfs(g: Graph, s: T) -> Tuple[dict, dict, dict]:
    queue = deque()
    marked = {s: True}
    dist = {s: 0}
    edge = {}
    queue.append(s)
    while queue:
        v = queue.popleft()
        for e in neighbors(g, v):
            w = e.right
            if not marked.get(w, False):
                marked[w] = True
                edge[w] = v
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist, edge, marked


def dfs(g: Graph, v: T) -> list: 
    edge = []
    def _dfs(u, visited):
        visited.append(u)
        adj = neighbors(g, u)
        while len(adj) > 0:
            w = adj.pop().right
            if not w in visited:
                _dfs(w, visited.copy())
        edge.append(visited)
    
    _dfs(v, []) 
    return edge

