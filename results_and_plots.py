import matplotlib.pyplot as plt

DIFFICULTY_ORDER = ["Easy", "Medium", "Hard", "Worst"]

def make_metrics(nodes, lengths):
    return {
        difficulty: {"nodes": nodes[index], "length": lengths[index]}
        for index, difficulty in enumerate(DIFFICULTY_ORDER)
    }

ALGORITHM_RESULTS = {
    ("Iterative Deepening", "N/A"): {
        "Easy": {"nodes": 334.1, "length": 7.0},
        "Medium": {"nodes": 28269.0, "length": 15.0},
        "Hard": {"nodes": 695113.1, "length": 21.0},
        "Worst": {"nodes": 134381277.0, "length": 31.0},
    },
    ("Uniform Cost", "Tiles Out of Place"): make_metrics(
        nodes=[143.7, 6407.25, 72320.5, 181315.7],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
    ("Uniform Cost", "Tiles Out of Row/Column"): make_metrics(
        nodes=[143.7, 6407.25, 72320.5, 181315.7],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
    ("Uniform Cost", "Manhattan Distance"): make_metrics(
        nodes=[143.7, 6407.25, 72320.5, 181315.7],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
    ("Greedy Best-First", "Tiles Out of Place"): make_metrics(
        nodes=[52.675, 624.8, 716.2, 771.55],
        lengths=[10.7, 75.9, 94.55, 100.75],
    ),
    ("Greedy Best-First", "Tiles Out of Row/Column"): make_metrics(
        nodes=[2035.4, 8066.777777777777, 3187.5, 12043.708333333334],
        lengths=[59.25, 154.11111111111111, 168.0, 156.66666666666666],
    ),
    ("Greedy Best-First", "Manhattan Distance"): make_metrics(
        nodes=[1797.175, 4150.8, 4295.375, 5444.55],
        lengths=[51.2, 79.5, 102.7, 101.7],
    ),
    ("A*", "Tiles Out of Place"): make_metrics(
        nodes=[13.35, 341.175, 4887.875, 100266.5],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
    ("A*", "Tiles Out of Row/Column"): make_metrics(
        nodes=[35.925, 1285.675, 15238.45, 147064.0],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
    ("A*", "Manhattan Distance"): make_metrics(
        nodes=[41.1, 1176.025, 11163.95, 116303.125],
        lengths=[7.0, 15.0, 21.0, 30.05],
    ),
}

def _series_from_metrics(metrics):
    lengths = [metrics[difficulty]["length"] for difficulty in DIFFICULTY_ORDER]
    nodes = [metrics[difficulty]["nodes"] for difficulty in DIFFICULTY_ORDER]
    return lengths, nodes

def plot_per_algorithm(results, baseline_key=("Iterative Deepening", "N/A")):
    algorithms = ["Iterative Deepening", "Uniform Cost", "Greedy Best-First", "A*"]
    baseline_lengths, baseline_nodes = _series_from_metrics(results[baseline_key])

    for algorithm in algorithms:
        plt.figure(figsize=(8, 5))
        plt.yscale("log")
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.xlabel("Solution Length (# moves)")
        plt.ylabel("Nodes Expanded")

        if algorithm == "Iterative Deepening":
            lengths, nodes = _series_from_metrics(results[(algorithm, "N/A")])
            plt.plot(lengths, nodes, marker="o", label="Iterative Deepening")
        else:
            combos = [
                key for key in results.keys() if key[0] == algorithm
            ]
            for alg_key in combos:
                heuristic = alg_key[1]
                lengths, nodes = _series_from_metrics(results[alg_key])
                plt.plot(
                    lengths,
                    nodes,
                    marker="o",
                    label=heuristic,
                )
            plt.plot(
                baseline_lengths,
                baseline_nodes,
                marker="o",
                linestyle="--",
                color="black",
                label="Iterative Deepening",
            )

        plt.title(f"{algorithm} Performance by Difficulty")
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    plot_per_algorithm(ALGORITHM_RESULTS)
