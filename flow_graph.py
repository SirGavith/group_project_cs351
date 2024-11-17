from __future__ import annotations
from collections import deque
from typing import List, Dict, Optional


class Edge:
    def __init__(self, target: Node, capacity: float) -> None:
        self.target = target
        self.capacity = capacity
        self.flow = 0
        self.reverse: Optional[Edge] = None  # Reverse edge reference


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edges: List[Edge] = []  # List of edges connected to this node

    def add_edge(self, target: Node, capacity: float) -> None:

        forward_edge = Edge(target, capacity)
        reverse_edge = Edge(self, 0)  # Reverse edge has 0 capacity initially

        forward_edge.reverse = reverse_edge
        reverse_edge.reverse = forward_edge

        self.edges.append(forward_edge)
        target.edges.append(reverse_edge)


class Graph:
    def __init__(self, nodes: Dict[str, Node]) -> None:
        self.nodes = nodes

    def bfs(self, source: Node, sink: Node) -> Optional[Dict[Node, Edge]]:
        """
        Perform BFS to find an augmenting path from source to sink.
        Returns a dictionary mapping each node to the edge used to reach it,
        or None if no path exists.
        """
        parent_map = {}
        queue = deque([source])

        while queue:
            current = queue.popleft()

            for edge in current.edges:
                residual_capacity = edge.capacity - edge.flow
                if edge.target not in parent_map and residual_capacity > 0:
                    parent_map[edge.target] = edge
                    if edge.target == sink:
                        return parent_map
                    queue.append(edge.target)

        return None

    def edmonds_karp(self, source: Node, sink: Node) -> float:
        max_flow = 0

        while True:
            # Find an augmenting path using BFS
            parent_map = self.bfs(source, sink)
            if not parent_map:  # No more augmenting paths
                break

            # Calculate bottleneck capacity (minimum residual capacity on the path)
            path_flow = float('inf')
            current = sink
            while current != source:
                edge = parent_map[current]
                path_flow = min(path_flow, edge.capacity - edge.flow)
                current = edge.reverse.target

            # Augment flow along the path
            current = sink
            while current != source:
                edge = parent_map[current]
                edge.flow += path_flow
                edge.reverse.flow -= path_flow
                current = edge.reverse.target

            # Add path flow to max flow
            max_flow += path_flow

        return max_flow