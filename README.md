# Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Project type:** Python coding-based capstone prototype  
**University brief:** K.R. Mangalam University - Mini-Courier Planner

## 1. Project overview

Mini-Courier Planner is an integrated Python prototype for planning one courier delivery trip. It combines four algorithmic components from the capstone brief:

1. **Merge Sort** - prioritizes parcels by priority rank and then delivery deadline. Priority `1` means the most urgent.
2. **0/1 Knapsack using Dynamic Programming** - chooses a set of parcels with maximum total `value_score` without exceeding the vehicle's weight capacity. Each parcel can be selected once.
3. **Dijkstra's Algorithm** - calculates shortest road distances and paths between the depot and selected customer locations.
4. **Nearest Neighbor TSP heuristic** - chooses an approximate order in which the selected customer locations should be visited, returning to the depot at the end.

The sample input is fictional and is included to demonstrate the program. Distances are illustrative kilometres, not live map data.

## 2. Project structure

```text
Mini-Courier-Planner/
├── main.py                         # Runs the integrated courier planner
├── benchmark.py                    # Measures runtimes and creates charts
├── run_tests.py                    # Runs the unit tests
├── requirements.txt                # Python package requirements
├── courier_planner/
│   ├── __init__.py
│   ├── sorting.py                   # Merge Sort and parcel prioritization
│   ├── knapsack.py                  # 0/1 Knapsack DP
│   ├── graph.py                    # Weighted graph and Dijkstra
│   ├── tsp.py                       # Distance matrix and Nearest Neighbor TSP
│   ├── data_io.py                  # CSV loading and validation
│   └── planner.py                  # Integrates all algorithms
├── data/
│   ├── parcels.csv                 # Sample parcel records
│   ├── locations.csv               # Depot and customer locations
│   └── roads.csv                   # Road edges and distances
├── tests/
│   └── test_algorithms.py          # Unit tests for the algorithms
├── results/
│   ├── demo_output.txt             # Output from the sample run
│   ├── test_results.txt            # Unit-test evidence
│   ├── benchmark_output.txt        # Benchmark console output
│   ├── runtime_results.csv         # Runtime measurements
│   ├── screenshots/                # Output evidence images
│   └── runtime_charts/             # Runtime charts
└── report/
    ├── Mini_Courier_Planner_Report.docx
    └── Mini_Courier_Planner_Report.pdf
```

## 3. Requirements

- Python 3.10 or newer is recommended.
- `matplotlib` is required only for generating runtime charts.
- No database, API key, internet connection, or external map service is required.

## 4. Setup

Open Terminal in the project folder.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Run the project

From the project root, execute:

```bash
python main.py
```

The program reads the three CSV files in `data/`, prints the complete delivery plan, and saves the same output to `results/demo_output.txt`.

Optional arguments:

```bash
python main.py --capacity 20
python main.py --capacity 18 --depot WH --data-dir data
python main.py --capacity 18 --output results/my_run.txt
```

- `--capacity`: maximum vehicle weight in integer kilograms (default: `18`).
- `--depot`: starting and ending depot node ID (default: `WH`).
- `--data-dir`: folder containing the three CSV files (default: `data`).
- `--output`: output text file path (default: `results/demo_output.txt`).

## 6. Run tests

```bash
python run_tests.py
```

The included tests cover sorting order, parcel priority tie-breaking, knapsack capacity and value, Dijkstra shortest paths, and a closed nearest-neighbor tour.

## 7. Run performance experiments

```bash
python benchmark.py
```

The benchmark uses deterministic, generated test inputs and measures the median of five runs for each input size. It writes:

- `results/runtime_results.csv`
- `results/runtime_charts/merge_sort_runtime.png`
- `results/runtime_charts/knapsack_runtime.png`
- `results/runtime_charts/dijkstra_runtime.png`
- `results/runtime_charts/nearest_neighbor_tsp_runtime.png`

The benchmark input sizes are different for each algorithm because their input dimensions differ. For knapsack, capacity is held at 250 kg while the number of parcels changes. Dijkstra uses connected sparse graphs. TSP is measured on a complete distance matrix.

## 8. Input data format

### `data/parcels.csv`

| Column | Meaning |
|---|---|
| `parcel_id` | Unique parcel identifier |
| `weight_kg` | Parcel weight; positive integer kilograms |
| `priority` | Priority rank; 1 is highest |
| `deadline_hours` | Hours remaining until delivery deadline |
| `value_score` | Non-negative integer reward used by knapsack |
| `delivery_node` | Location ID where the parcel must be delivered |

The sorting rule is `(priority ascending, deadline_hours ascending)`. The knapsack objective is to maximize the sum of `value_score`, subject to the vehicle capacity. These are separate decisions in this prototype.

### `data/locations.csv`

- `node_id`: unique graph node identifier.
- `name`: readable location name.
- `location_type`: `depot` or `customer`.

### `data/roads.csv`

- `from_node` and `to_node`: endpoint node IDs.
- `distance_km`: positive road distance in kilometres.

Roads are treated as undirected. All road weights must be non-negative for Dijkstra; the sample file uses positive values.

## 9. Sample result

Using the supplied sample CSV files and an 18 kg vehicle:

- 12 parcels are prioritized.
- The selected parcel set is `P003, P010, P001, P006, P008, P011`.
- Total selected weight is **17 kg**; unused capacity is **1 kg**.
- Total selected value score is **535**.
- The nearest-neighbor delivery stop order is `WH -> A -> C -> D -> E -> F -> WH`.
- The expanded road path is `WH -> A -> B -> C -> D -> E -> F -> G -> WH`.
- Total road distance is **26.00 km**.

These values are expected for the included data and default settings. Changing CSV data or capacity can change the result.

## 10. Complexity summary

Let `n` be the number of parcels, `W` the integer vehicle capacity, `V` the number of road graph nodes, `E` the number of road edges, and `k` the number of delivery stops including the depot.

| Component | Time complexity | Space complexity |
|---|---|---|
| Merge Sort | `O(n log n)` | `O(n)` auxiliary |
| 0/1 Knapsack DP | `O(nW)` | `O(nW)` for the DP table |
| Dijkstra with a binary heap | `O((V + E) log V)` | `O(V + E)` |
| Nearest Neighbor TSP | `O(k^2)` | `O(k)` excluding the distance matrix |
| Repeated Dijkstra for all selected stops | `O(k(V + E) log V)` | `O(kV)` for the matrix and path cache |

## 11. Assumptions and limitations

- This is a prototype for one depot and one vehicle trip, not a production courier platform.
- Weights and knapsack capacity are integer kilograms. Fractional weights are not supported by the DP table implementation.
- The sample roads are static, undirected, and have fixed distances. Traffic, one-way roads, tolls, and live maps are not modelled.
- The nearest-neighbor TSP method is a heuristic. It quickly constructs a valid tour but does not guarantee the globally shortest possible tour.
- Parcels for the same customer location are delivered in one stop.
- The knapsack selects by `value_score`; priority and deadline are used for the displayed parcel sorting. A production system could combine urgency, penalties, and service-level constraints into the objective function.
- Runtime measurements depend on the machine and Python environment. They are observations, not universal benchmark values.

## 12. Suggested viva points

Be ready to explain why Merge Sort is suitable for sorting, how the DP table decides whether to include a parcel, why Dijkstra needs non-negative edges, how the nearest-neighbor heuristic chooses the next stop, and why a heuristic tour may not be optimal. Also be ready to trace one small input by hand and change the capacity or CSV records during the demonstration.

---

**Before submission:** fill in your name, roll number, and any required class details in the report. Confirm the actual deadline and upload the ZIP or GitHub link through the method specified by your faculty/Zosima.
