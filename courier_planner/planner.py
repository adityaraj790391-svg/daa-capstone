"""Integration layer that combines sorting, knapsack, Dijkstra and TSP."""

from __future__ import annotations

from typing import Any

from .graph import WeightedGraph
from .knapsack import knapsack_01
from .sorting import prioritize_parcels
from .tsp import build_distance_matrix, expand_tour, nearest_neighbor_tsp


def create_delivery_plan(
    parcels: list[dict[str, Any]],
    locations: dict[str, dict[str, str]],
    roads: list[tuple[str, str, float]],
    depot: str,
    capacity_kg: int,
) -> dict[str, Any]:
    """Generate prioritized parcel list, packing plan and delivery route."""
    if depot not in locations:
        raise ValueError(f"Depot {depot} is not in the location data.")

    prioritized = prioritize_parcels(parcels)
    selected, total_value, dp_table = knapsack_01(prioritized, capacity_kg)
    total_weight = sum(int(parcel["weight_kg"]) for parcel in selected)

    graph = WeightedGraph.from_edges(locations.keys(), roads)
    delivery_stops = sorted({parcel["delivery_node"] for parcel in selected})
    stops = [depot] + [node for node in delivery_stops if node != depot]

    if len(stops) == 1:
        route = [depot, depot]
        route_distance = 0.0
        expanded_route = [depot]
        distance_matrix: dict[str, dict[str, float]] = {depot: {depot: 0.0}}
    else:
        distance_matrix, path_cache = build_distance_matrix(graph, stops)
        route, route_distance = nearest_neighbor_tsp(stops, distance_matrix, depot)
        expanded_route = expand_tour(route, path_cache)

    # Validate that the route is a closed trip and the selected load fits.
    if total_weight > capacity_kg:
        raise AssertionError("Knapsack returned a load above vehicle capacity.")
    if route[0] != depot or route[-1] != depot:
        raise AssertionError("Delivery route must start and finish at the depot.")

    return {
        "prioritized_parcels": prioritized,
        "selected_parcels": selected,
        "total_weight_kg": total_weight,
        "capacity_kg": capacity_kg,
        "total_value": total_value,
        "dp_table": dp_table,
        "delivery_stops": stops,
        "stop_route": route,
        "expanded_route": expanded_route,
        "route_distance_km": route_distance,
        "distance_matrix": distance_matrix,
        "locations": locations,
    }
