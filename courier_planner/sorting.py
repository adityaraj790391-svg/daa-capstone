"""Stable merge sort for parcel prioritization."""

from __future__ import annotations

from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")


def merge_sort(items: Iterable[T], key: Callable[[T], Any]) -> list[T]:
    """Return items in ascending key order using stable merge sort.

    The merge is stable: when keys are equal, the item from the left half
    remains first. Time complexity: O(n log n); extra space: O(n).
    """
    values = list(items)
    if len(values) <= 1:
        return values

    middle = len(values) // 2
    left = merge_sort(values[:middle], key)
    right = merge_sort(values[middle:], key)
    return _merge(left, right, key)


def _merge(left: list[T], right: list[T], key: Callable[[T], Any]) -> list[T]:
    merged: list[T] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def prioritize_parcels(parcels: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort parcels by priority (1 is highest), then earliest deadline."""
    return merge_sort(
        parcels,
        key=lambda parcel: (int(parcel["priority"]), float(parcel["deadline_hours"])),
    )
