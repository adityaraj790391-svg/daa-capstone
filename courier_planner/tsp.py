"""Nearest-neighbor TSP heuristic over shortest-path distances."""

from __future__ import annotations

import math
from typing import Mapping, Sequence


def nearest_neighbor_tsp(
    locations: Sequence[str], distance_matrix: Mapping[str, Mapping[str, float]], start: str
) -> tuple[list[str], float]:
    """Build a closed tour using the nearest unvisited location each time.

    The input matrix should contain shortest-path distances between every pair
    of delivery stops. This is a heuristic, not an exact TSP solver.
    Time complexity: O(k^2); extra space: O(k).
    """
    unique_locations = list(dict.fromkeys(locations))
    if start not in unique_locations:
        raise ValueError("The start location must be included in locations.")
    if len(unique_locations) == 1:
        return [start, start], 0.0

    unvisited = set(unique_locations)
    unvisited.remove(start)
    route = [start]
    total_distance = 0.0
    current = start

    while unvisited:
        candidates = []
        for candidate in unvisited:
            distance = distance_matrix.get(current, {}).get(candidate, math.inf)
            candidates.append((distance, candidate))
        next_distance, next_location = min(candidates)
        if math.isinf(next_distance):
            raise ValueError(f"No route exists from {current} to any remaining location.")
        total_distance += next_distance
        route.append(next_location)
        unvisited.remove(next_location)
        current = next_location

    return_distance = distance_matrix.get(current, {}).get(start, math.inf)
    if math.isinf(return_distance):
        raise ValueError(f"No return route exists from {current} to {start}.")
    total_distance += return_distance
    route.append(start)
    return route, total_distance


def build_distance_matrix(graph, stops: Sequence[str]) -> tuple[dict[str, dict[str, float]], dict[tuple[str, str], list[str]]]:
    """Run Dijkstra from each stop to create a metric closure and path cache."""
    matrix: dict[str, dict[str, float]] = {}
    path_cache: dict[tuple[str, str], list[str]] = {}
    for source in stops:
        distances, previous = graph.dijkstra(source)
        matrix[source] = {}
        for destination in stops:
            matrix[source][destination] = distances[destination]
            path_cache[(source, destination)] = graph.reconstruct_path(
                previous, source, destination
            ) if not math.isinf(distances[destination]) else []
    return matrix, path_cache


def expand_tour(route: Sequence[str], path_cache: Mapping[tuple[str, str], list[str]]) -> list[str]:
    """Expand a stop tour into the road-node path between consecutive stops."""
    if len(route) < 2:
        return list(route)
    expanded: list[str] = []
    for source, destination in zip(route, route[1:]):
        segment = path_cache.get((source, destination), [])
        if not segment:
            raise ValueError(f"Missing shortest path from {source} to {destination}.")
        if expanded:
            expanded.extend(segment[1:])
        else:
            expanded.extend(segment)
    return expanded
