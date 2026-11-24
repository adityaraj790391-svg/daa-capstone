"""Weighted undirected graph and Dijkstra shortest-path algorithm."""

from __future__ import annotations

import heapq
import math
from collections import defaultdict
from typing import Iterable


class WeightedGraph:
    """Adjacency-list graph with non-negative edge weights."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)

    def add_node(self, node: str) -> None:
        self.adjacency[node]  # Ensure the node exists.

    def add_edge(self, source: str, destination: str, distance: float) -> None:
        if distance < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative weights.")
        self.add_node(source)
        self.add_node(destination)
        self.adjacency[source].append((destination, float(distance)))
        self.adjacency[destination].append((source, float(distance)))

    @classmethod
    def from_edges(cls, nodes: Iterable[str], edges: Iterable[tuple[str, str, float]]) -> "WeightedGraph":
        graph = cls()
        for node in nodes:
            graph.add_node(node)
        for source, destination, distance in edges:
            graph.add_edge(source, destination, distance)
        return graph

    def dijkstra(self, start: str) -> tuple[dict[str, float], dict[str, str | None]]:
        """Return shortest distances and predecessor map from start.

        Complexity with a binary heap and adjacency lists:
        O((V + E) log V).
        """
        if start not in self.adjacency:
            raise KeyError(f"Unknown starting node: {start}")

        distances = {node: math.inf for node in self.adjacency}
        previous: dict[str, str | None] = {node: None for node in self.adjacency}
        distances[start] = 0.0
        priority_queue: list[tuple[float, str]] = [(0.0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue

            for neighbor, edge_distance in self.adjacency[current_node]:
                new_distance = current_distance + edge_distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances, previous

    @staticmethod
    def reconstruct_path(
        previous: dict[str, str | None], start: str, destination: str
    ) -> list[str]:
        """Reconstruct a path from a Dijkstra predecessor map."""
        if start == destination:
            return [start]
        path: list[str] = []
        current: str | None = destination
        while current is not None:
            path.append(current)
            if current == start:
                path.reverse()
                return path
            current = previous.get(current)
        return []

    def shortest_path(self, start: str, destination: str) -> tuple[float, list[str]]:
        distances, previous = self.dijkstra(start)
        distance = distances.get(destination, math.inf)
        if math.isinf(distance):
            return distance, []
        return distance, self.reconstruct_path(previous, start, destination)
