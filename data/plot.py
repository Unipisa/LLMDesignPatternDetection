import sys
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.pyplot as plt
import os
import textwrap


"""
Calcola tutti i plot necessari salvandoli dove opportuno
"""

METRIC_COLORS = {
    "BNPS": "steelblue",
    "acc_top1": "darkorange",
    "false_positive_rate": "seagreen",
    "precision@1": "mediumpurple",
    "positional_similarity": "crimson",
    "ndcg_standard": "gold",
    "ndcg_inverted": "saddlebrown"
}

METRICS = ["precision@1", "BNPS", "false_positive_rate", "acc_top1", "positional_similarity",
           "ndcg_standard", "ndcg_inverted"]


def plot_prompt_performance(df):
    to_plot = df.groupby("prompt_label")[METRICS].mean()
    to_plot = to_plot.T
    ax = to_plot.plot.bar(figsize=(15, 10))
    labels = [textwrap.fill(label.get_text(), width=15) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0)
    plt.yticks([i/10 for i in range(0, 12, 2)])
    ax.legend(loc='best')
    plt.title("Average performance per prompt", loc = "center")
    plt.rcParams['figure.dpi'] = 300    # increases chart's resolution
    output_path = "plots/prompt_performance.png"
    plt.grid(True)
    plt.savefig(output_path)


def plot_model_shot_performance(df):
    to_plot = df.groupby(["model", "shot"]).agg(
        avg_precision_1=("precision@1", "mean"),
        avg_bnps=("BNPS", "mean"),
        avg_false_positive_rate=("false_positive_rate", "mean"),
        avg_acc_top1=("acc_top1", "mean"),
        avg_positional_similarity=("positional_similarity", "mean"),
        avg_ndcg_standard=("ndcg_standard", "mean"),
        avg_ndcg_inverted=("ndcg_inverted", "mean")
    )
    ax = to_plot.plot.bar(figsize=(15, 10), y=["avg_precision_1", "avg_bnps", "avg_acc_top1", "avg_false_positive_rate"])
    labels = [textwrap.fill(label.get_text(), width=15) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0)
    plt.yticks([i / 10 for i in range(0, 12, 2)])
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3, fontsize= 6)
    ax.legend(loc='best', bbox_to_anchor=(1.01, 1))
    plt.title("Average model-shot performance", loc="center")
    plt.rcParams['figure.dpi'] = 300  # increases chart's resolution
    output_path = "plots/model-shot_performance.png"
    plt.grid(True)
    plt.savefig(output_path)


def plot_design_patterns_performance():
    best_confs = ["gemma-4-e4b_zero-shot_id5_temp0.0.csv", "qwen3.5-9b_one-shot_id2_temp0.7.csv", "gpt-oss-20b_one-shot_id0_temp0.0.csv"]
    names = {
        "gemma-4-e4b_zero-shot_id5_temp0.0.csv": "gemma-4-e4b_zero-shot_id5_temp0.0",
        "qwen3.5-9b_one-shot_id2_temp0.7.csv": "qwen3.5-9b_one-shot_id2_temp0.7",
        "gpt-oss-20b_one-shot_id0_temp0.0.csv": "gpt-oss-20b_one-shot_id0_temp0.0"
    }
    for best_conf in best_confs:
        # average results extraction for each conf.
        base_dir = "results/evaluated"
        run_dirs = [d for d in os.listdir(base_dir) if d.startswith("run_") and os.path.isfile(os.path.join(base_dir, d,  best_conf))]
        if not run_dirs:
            print(f"No run found for {best_conf}", file=sys.stderr)
            continue

        frames = []
        for run_dir in run_dirs:
            tmp = pd.read_csv(os.path.join(base_dir, run_dir, best_conf))
            tmp["id"] = tmp["id"].astype(int)
            frames.append(tmp)

        df = pd.concat(frames).groupby("id")[["BNPS", "acc_top1"]].mean()       # average results!
        color = [METRIC_COLORS[m] for m in ["BNPS", "acc_top1"]]
        ax = df.plot.bar(figsize=(15, 8), y=["BNPS", "acc_top1"], color=color)

        bar_handles, bar_labels = ax.get_legend_handles_labels()        # legend for columns
        ids = list(df.index)  # lista ordinata degli id nel grafico

        categories = {
            "Behavioural": [i for i, v in enumerate(ids) if v <= 10],
            "Creational": [i for i, v in enumerate(ids) if 13 <= v <= 19],
            "Structural": [i for i, v in enumerate(ids) if v >= 22],
        }
        colors = {"Behavioural": "steelblue", "Creational": "seagreen", "Structural": "tomato"}

        for cat, pos in categories.items():
            if pos:
                ax.axvspan(pos[0] - 0.5, pos[-1] + 0.5,
                           alpha=0.5, color=colors[cat], label=cat, zorder=0)


        area_patches = [mpatches.Patch(color=col, alpha=0.35, label=cat)
                        for cat, col in colors.items()]     # creates legend manually


        ax.legend(
            handles=bar_handles + area_patches,
            labels=bar_labels + list(colors.keys()),
            loc="best",
            bbox_to_anchor=(1.01, 1)
        ) # place legend

        plt.grid(True)

        plt.xticks(rotation=0)
        plt.title(f"Performance per design pattern — {names[best_conf]} (best configuration)", loc="center")
        plt.rcParams['figure.dpi'] = 300
        output_path = f"plots/design-patterns-performance_{names[best_conf]}.png"
        plt.savefig(output_path)

def plot_stability():

    rows = []
    # average results extraction for each conf.
    base_dir = "avg_results/runs_avg_results"
    if not os.path.exists(base_dir):
        print(f"{base_dir} does not exist", file=sys.stderr)
        exit(1)
    if not os.path.isdir(base_dir):
        print(f"{base_dir} is not a directory", file=sys.stderr)
        exit(1)

    rows = []
    for run_avg_results in os.listdir(base_dir):
        if not run_avg_results.endswith(".csv"):
            print(f"{run_avg_results} is not a csv file", file=sys.stderr)
            continue

        tmp = pd.read_csv(os.path.join(base_dir, run_avg_results))
        tmp[METRICS] = tmp[METRICS].astype(float)
        tmp = tmp.groupby("model")[METRICS].mean()      # avg performance per run
        rows.append(tmp)

    combine = pd.concat(rows)

    # average results per run
    std = combine.groupby("model").std()       # std between runs, on std per metric: it's a Pandas series with index=metrics
    std = std.T         # models are now columns, metrics on rows
    ax = std.plot.bar(figsize=(15, 8))
    for container in ax.containers:
        ax.bar_label(container, fmt="%.4f", padding=3, fontsize= 5)

    plt.xticks(rotation=0)
    plt.grid(True)
    plt.title("Stability across runs — Standard deviation per model")
    plt.ylabel("Standard deviation")
    plt.rcParams['figure.dpi'] = 300
    output_path = "plots/stability-across-runs.png"
    plt.savefig(output_path)



if __name__ == "__main__":
    dir_to_process = "avg_results"
    total_avg_results = os.path.join(dir_to_process, "total_avg_results.csv")
    if not os.path.exists(dir_to_process):
        print(f"{dir_to_process} doesn't exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(dir_to_process):
        print(f"{dir_to_process} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(total_avg_results):
        print(total_avg_results, "doesn't exist", file=sys.stderr)
        sys.exit(1)

    data = pd.read_csv(total_avg_results)
    plot_prompt_performance(data)
    plot_model_shot_performance(data)
    plot_design_patterns_performance()
    plot_stability()