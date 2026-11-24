"""Benchmark the main algorithms and generate CSV results and runtime charts."""

from __future__ import annotations

import csv
import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from courier_planner.graph import WeightedGraph
from courier_planner.knapsack import knapsack_01
from courier_planner.sorting import merge_sort
from courier_planner.tsp import nearest_neighbor_tsp

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
CHARTS = RESULTS / "runtime_charts"


def median_runtime_ms(function, repeats: int = 5) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def benchmark_sorting() -> list[tuple[str, int, float]]:
    rng = random.Random(42)
    rows = []
    for size in [100, 500, 1000, 2500, 5000, 10000]:
        values = [{"priority": rng.randint(1, 5), "deadline": rng.randint(1, 72), "id": i}
                  for i in range(size)]
        elapsed = median_runtime_ms(lambda: merge_sort(values, key=lambda x: (x["priority"], x["deadline"])))
        rows.append(("Merge Sort", size, elapsed))
    return rows


def benchmark_knapsack() -> list[tuple[str, int, float]]:
    rng = random.Random(43)
    rows = []
    capacity = 250
    for size in [20, 40, 80, 120, 160, 200]:
        parcels = [
            {"parcel_id": f"K{i}", "weight_kg": rng.randint(1, 30), "value_score": rng.randint(10, 100)}
            for i in range(size)
        ]
        elapsed = median_runtime_ms(lambda: knapsack_01(parcels, capacity))
        rows.append(("0/1 Knapsack DP", size, elapsed))
    return rows


def make_sparse_graph(node_count: int, seed: int = 44) -> WeightedGraph:
    rng = random.Random(seed + node_count)
    nodes = [f"N{i:04d}" for i in range(node_count)]
    edges: list[tuple[str, str, float]] = []
    # A chain guarantees connectivity.
    for i in range(node_count - 1):
        edges.append((nodes[i], nodes[i + 1], rng.randint(1, 20)))
    # Add short-range random links to form a sparse road network.
    for i in range(node_count):
        for _ in range(3):
            j = rng.randrange(node_count)
            if i != j:
                edges.append((nodes[i], nodes[j], rng.randint(1, 30)))
    return WeightedGraph.from_edges(nodes, edges)


def benchmark_dijkstra() -> list[tuple[str, int, float]]:
    rows = []
    for size in [30, 60, 120, 240, 480]:
        graph = make_sparse_graph(size)
        elapsed = median_runtime_ms(lambda: graph.dijkstra("N0000"))
        rows.append(("Dijkstra", size, elapsed))
    return rows


def make_distance_matrix(size: int, seed: int = 45) -> dict[str, dict[str, float]]:
    rng = random.Random(seed + size)
    names = [f"S{i:03d}" for i in range(size)]
    matrix = {name: {} for name in names}
    for i, source in enumerate(names):
        matrix[source][source] = 0.0
        for destination in names[i + 1:]:
            value = float(rng.randint(1, 100))
            matrix[source][destination] = value
            matrix[destination][source] = value
    return matrix


def benchmark_tsp() -> list[tuple[str, int, float]]:
    rows = []
    for size in [10, 20, 40, 80, 120, 160]:
        matrix = make_distance_matrix(size)
        stops = list(matrix)
        elapsed = median_runtime_ms(lambda: nearest_neighbor_tsp(stops, matrix, stops[0]))
        rows.append(("Nearest Neighbor TSP", size, elapsed))
    return rows


def save_chart(rows: list[tuple[str, int, float]], filename: str, title: str, x_label: str) -> None:
    sizes = [row[1] for row in rows]
    times = [row[2] for row in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times, marker="o")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Median execution time (milliseconds)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / filename, dpi=180)
    plt.close()


def main() -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    all_rows = benchmark_sorting() + benchmark_knapsack() + benchmark_dijkstra() + benchmark_tsp()
    csv_path = RESULTS / "runtime_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["algorithm", "input_size", "median_runtime_ms"])
        writer.writerows(all_rows)

    groups = {
        "sorting": [row for row in all_rows if row[0] == "Merge Sort"],
        "knapsack": [row for row in all_rows if row[0] == "0/1 Knapsack DP"],
        "dijkstra": [row for row in all_rows if row[0] == "Dijkstra"],
        "tsp": [row for row in all_rows if row[0] == "Nearest Neighbor TSP"],
    }
    save_chart(groups["sorting"], "merge_sort_runtime.png", "Merge Sort Runtime", "Number of parcels")
    save_chart(groups["knapsack"], "knapsack_runtime.png", "0/1 Knapsack DP Runtime", "Number of parcels (capacity fixed at 250 kg)")
    save_chart(groups["dijkstra"], "dijkstra_runtime.png", "Dijkstra Runtime on Sparse Graphs", "Number of graph nodes")
    save_chart(groups["tsp"], "nearest_neighbor_tsp_runtime.png", "Nearest Neighbor TSP Runtime", "Number of delivery stops")

    print("Benchmark completed. Median times in milliseconds:")
    print(f"Results saved to: {csv_path.relative_to(ROOT)}")
    for algorithm, size, elapsed in all_rows:
        print(f"{algorithm:22s} n={size:5d}  {elapsed:10.4f} ms")
    print(f"Charts saved to: {CHARTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
