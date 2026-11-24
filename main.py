"""Run the Mini-Courier Planner demo from the project root."""

from __future__ import annotations

import argparse
from pathlib import Path

from courier_planner.data_io import load_project_data
from courier_planner.planner import create_delivery_plan


def format_location(node_id: str, locations: dict[str, dict[str, str]]) -> str:
    details = locations[node_id]
    return f"{node_id} ({details['name']})"


def print_plan(plan: dict, save_to: Path | None = None) -> str:
    locations = plan["locations"]
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("                 MINI-COURIER PLANNER - DEMONSTRATION")
    lines.append("=" * 72)
    lines.append("\n1. PARCEL PRIORITIZATION (Merge Sort)")
    lines.append("   Priority: 1 is the highest; earlier deadline breaks a tie.")
    lines.append("   " + " | ".join(
        f"{p['parcel_id']}: P{p['priority']}, {p['deadline_hours']:g}h"
        for p in plan["prioritized_parcels"]
    ))

    lines.append("\n2. VEHICLE PACKING (0/1 Knapsack - Dynamic Programming)")
    lines.append(f"   Vehicle capacity : {plan['capacity_kg']} kg")
    lines.append("   Selected parcels : " + ", ".join(p["parcel_id"] for p in plan["selected_parcels"]))
    lines.append(f"   Total load       : {plan['total_weight_kg']} kg")
    lines.append(f"   Unused capacity  : {plan['capacity_kg'] - plan['total_weight_kg']} kg")
    lines.append(f"   Total value score: {plan['total_value']}")

    lines.append("\n   DP table (rows = parcels considered; columns = capacity 0..W):")
    dp = plan["dp_table"]
    if len(dp) <= 16 and len(dp[0]) <= 26:
        lines.append("      " + " ".join(f"{i:>3}" for i in range(len(dp[0]))))
        for row_index, row in enumerate(dp):
            lines.append(f"   {row_index:>2}: " + " ".join(f"{value:>3}" for value in row))
    else:
        lines.append(f"      DP table computed: {len(dp)} x {len(dp[0])} cells (not expanded in console).")

    lines.append("\n3. SHORTEST PATHS AND DELIVERY ROUTE")
    lines.append("   Dijkstra is run from each selected stop to build shortest-path distances.")
    lines.append("   Delivery stop order (Nearest Neighbor TSP heuristic):")
    lines.append("   " + " -> ".join(format_location(node, locations) for node in plan["stop_route"]))
    lines.append("   Expanded road path:")
    lines.append("   " + " -> ".join(plan["expanded_route"]))
    lines.append(f"   Total route distance: {plan['route_distance_km']:.2f} km")

    lines.append("\n4. ALGORITHM COMPLEXITIES")
    lines.append("   Merge Sort          : O(n log n) time, O(n) extra space")
    lines.append("   0/1 Knapsack DP     : O(nW) time and O(nW) space")
    lines.append("   Dijkstra (heap)     : O((V + E) log V) time")
    lines.append("   Nearest Neighbor TSP: O(k^2) time, O(k) extra space")
    lines.append("\n" + "=" * 72)
    lines.append("Demo completed. See README.md and report/ for documentation.")
    output = "\n".join(lines) + "\n"
    print(output, end="")
    if save_to:
        save_to.parent.mkdir(parents=True, exist_ok=True)
        save_to.write_text(output, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-Courier Planner prototype")
    parser.add_argument("--capacity", type=int, default=18, help="Vehicle capacity in kg (default: 18)")
    parser.add_argument("--depot", default="WH", help="Depot node ID (default: WH)")
    parser.add_argument("--data-dir", default="data", help="Folder containing CSV input files")
    parser.add_argument("--output", default="results/demo_output.txt", help="Save console output to this file")
    args = parser.parse_args()

    if args.capacity < 0:
        parser.error("--capacity must be zero or greater")

    parcels, locations, roads = load_project_data(args.data_dir)
    plan = create_delivery_plan(parcels, locations, roads, args.depot, args.capacity)
    print_plan(plan, Path(args.output))


if __name__ == "__main__":
    main()
