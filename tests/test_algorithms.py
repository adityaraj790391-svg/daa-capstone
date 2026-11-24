"""Unit tests for the Mini-Courier Planner algorithms."""

import unittest

from courier_planner.graph import WeightedGraph
from courier_planner.knapsack import knapsack_01
from courier_planner.sorting import merge_sort, prioritize_parcels
from courier_planner.tsp import nearest_neighbor_tsp


class SortingTests(unittest.TestCase):
    def test_merge_sort_orders_values(self):
        self.assertEqual(merge_sort([5, 1, 4, 2], key=lambda x: x), [1, 2, 4, 5])

    def test_parcel_priority_and_deadline(self):
        parcels = [
            {"parcel_id": "P1", "priority": 2, "deadline_hours": 4},
            {"parcel_id": "P2", "priority": 1, "deadline_hours": 8},
            {"parcel_id": "P3", "priority": 1, "deadline_hours": 3},
        ]
        result = prioritize_parcels(parcels)
        self.assertEqual([p["parcel_id"] for p in result], ["P3", "P2", "P1"])


class KnapsackTests(unittest.TestCase):
    def test_knapsack_respects_capacity_and_maximizes_value(self):
        parcels = [
            {"parcel_id": "A", "weight_kg": 2, "value_score": 40},
            {"parcel_id": "B", "weight_kg": 3, "value_score": 50},
            {"parcel_id": "C", "weight_kg": 4, "value_score": 70},
        ]
        selected, total_value, _ = knapsack_01(parcels, 5)
        self.assertEqual(total_value, 90)
        self.assertEqual({p["parcel_id"] for p in selected}, {"A", "B"})
        self.assertLessEqual(sum(p["weight_kg"] for p in selected), 5)


class GraphTests(unittest.TestCase):
    def test_dijkstra_returns_shortest_path(self):
        graph = WeightedGraph.from_edges(
            ["A", "B", "C", "D"],
            [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 1), ("C", "D", 7)],
        )
        distance, path = graph.shortest_path("A", "D")
        self.assertEqual(distance, 4)
        self.assertEqual(path, ["A", "C", "B", "D"])


class TSPTests(unittest.TestCase):
    def test_nearest_neighbor_returns_to_start(self):
        matrix = {
            "W": {"W": 0, "A": 2, "B": 5},
            "A": {"W": 2, "A": 0, "B": 3},
            "B": {"W": 5, "A": 3, "B": 0},
        }
        route, distance = nearest_neighbor_tsp(["W", "A", "B"], matrix, "W")
        self.assertEqual(route[0], "W")
        self.assertEqual(route[-1], "W")
        self.assertEqual(set(route[:-1]), {"W", "A", "B"})
        self.assertEqual(distance, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
