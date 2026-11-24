"""0/1 Knapsack dynamic programming for vehicle parcel selection."""

from __future__ import annotations

from typing import Any


def knapsack_01(
    parcels: list[dict[str, Any]], capacity_kg: int
) -> tuple[list[dict[str, Any]], int, list[list[int]]]:
    """Choose a maximum-value subset without exceeding integer capacity.

    Each parcel can be selected at most once. Parcel weights must be positive
    integers in kilograms and value_score must be a non-negative integer.

    Returns (selected_parcels, total_value, dp_table).
    Time and space complexity: O(n * capacity).
    """
    if capacity_kg < 0:
        raise ValueError("Vehicle capacity cannot be negative.")

    normalized: list[tuple[int, int]] = []
    for parcel in parcels:
        weight = int(parcel["weight_kg"])
        value = int(parcel["value_score"])
        if weight <= 0:
            raise ValueError(f"Parcel {parcel.get('parcel_id', '?')} has invalid weight.")
        if value < 0:
            raise ValueError(f"Parcel {parcel.get('parcel_id', '?')} has negative value.")
        normalized.append((weight, value))

    n = len(parcels)
    dp = [[0 for _ in range(capacity_kg + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = normalized[i - 1]
        for remaining_capacity in range(capacity_kg + 1):
            dp[i][remaining_capacity] = dp[i - 1][remaining_capacity]
            if weight <= remaining_capacity:
                include_value = value + dp[i - 1][remaining_capacity - weight]
                if include_value > dp[i][remaining_capacity]:
                    dp[i][remaining_capacity] = include_value

    selected: list[dict[str, Any]] = []
    remaining_capacity = capacity_kg
    for i in range(n, 0, -1):
        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:
            selected.append(parcels[i - 1])
            remaining_capacity -= normalized[i - 1][0]

    selected.reverse()
    return selected, dp[n][capacity_kg], dp
