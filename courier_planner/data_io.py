"""CSV loading and validation helpers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


REQUIRED_PARCEL_FIELDS = {
    "parcel_id", "weight_kg", "priority", "deadline_hours", "value_score", "delivery_node"
}


def read_csv(path: str | Path) -> list[dict[str, str]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Required data file not found: {file_path}")
    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def load_parcels(path: str | Path) -> list[dict[str, Any]]:
    rows = read_csv(path)
    if not rows:
        raise ValueError("The parcel CSV contains no parcel records.")
    missing = REQUIRED_PARCEL_FIELDS - set(rows[0].keys())
    if missing:
        raise ValueError(f"Parcel CSV is missing columns: {', '.join(sorted(missing))}")

    parcels: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for row in rows:
        parcel_id = row["parcel_id"].strip()
        if not parcel_id or parcel_id in seen_ids:
            raise ValueError(f"Parcel IDs must be non-empty and unique: {parcel_id!r}")
        seen_ids.add(parcel_id)
        parcel = {
            "parcel_id": parcel_id,
            "weight_kg": int(row["weight_kg"]),
            "priority": int(row["priority"]),
            "deadline_hours": float(row["deadline_hours"]),
            "value_score": int(row["value_score"]),
            "delivery_node": row["delivery_node"].strip(),
        }
        if parcel["weight_kg"] <= 0:
            raise ValueError(f"Parcel {parcel_id} must have positive integer weight.")
        if parcel["priority"] < 1:
            raise ValueError(f"Parcel {parcel_id} priority must be 1 or greater.")
        if parcel["value_score"] < 0 or parcel["deadline_hours"] < 0:
            raise ValueError(f"Parcel {parcel_id} has an invalid score or deadline.")
        parcels.append(parcel)
    return parcels


def load_locations(path: str | Path) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    locations: dict[str, dict[str, str]] = {}
    for row in rows:
        node_id = row["node_id"].strip()
        if not node_id or node_id in locations:
            raise ValueError(f"Location IDs must be non-empty and unique: {node_id!r}")
        locations[node_id] = {
            "name": row["name"].strip(),
            "location_type": row["location_type"].strip(),
        }
    return locations


def load_roads(path: str | Path) -> list[tuple[str, str, float]]:
    rows = read_csv(path)
    roads: list[tuple[str, str, float]] = []
    for row in rows:
        distance = float(row["distance_km"])
        if distance <= 0:
            raise ValueError("Road distances must be positive.")
        roads.append((row["from_node"].strip(), row["to_node"].strip(), distance))
    return roads


def load_project_data(data_dir: str | Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, str]], list[tuple[str, str, float]]]:
    data_path = Path(data_dir)
    parcels = load_parcels(data_path / "parcels.csv")
    locations = load_locations(data_path / "locations.csv")
    roads = load_roads(data_path / "roads.csv")

    for parcel in parcels:
        if parcel["delivery_node"] not in locations:
            raise ValueError(
                f"Parcel {parcel['parcel_id']} refers to unknown location "
                f"{parcel['delivery_node']}."
            )
    for source, destination, _ in roads:
        if source not in locations or destination not in locations:
            raise ValueError(f"Road {source}-{destination} uses an unknown location.")
    return parcels, locations, roads
