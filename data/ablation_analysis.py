import sys, os, re
import textwrap
import matplotlib.pyplot as plt
import pandas as pd

from data.evaluate import false_positive_rate, positional_similarity

AVG_RUNS_RESULTS_PATH = "avg_results/runs_avg_results"
TABLES_DIR_PATH = "ablation/tables"
PLOTS_PATH = "ablation/plots"
BEST_PROMPT = "base + output description"
BEST_SHOT = "one-shot"
BEST_TEMPERATURE = None
BEST_MODEL = None

def load_runs():
    """
    Loads average results per each run and concatenates them in a unique dataframe
    """
    runs = []
    for filename in os.listdir(AVG_RUNS_RESULTS_PATH):
        if not filename.endswith(".csv"):
            print(f"{filename} is not a csv", file=sys.stderr)
            continue
        match = re.match(r"run_(\d+)_avg_results\.csv", filename)
        if not match:
            print(f"Error while extracring run id from {filename}", file=sys.stderr)
            continue
        run_id = int(match.group(1))

        run = pd.read_csv(os.path.join(AVG_RUNS_RESULTS_PATH, filename))
        run["run_id"] = run_id
        runs.append(run)

    if not runs:
        print(f"{AVG_RUNS_RESULTS_PATH} is empty", file=sys.stderr)
        sys.exit(1)
    data = pd.concat(runs)
    data.reset_index(drop=True, inplace=True)
    return data

def compute_config_stats(data):
    """
    Groups by prompt label, shot, model, temperature and computes mean and std per each metric.
    Adds a new "robust_BNPS" column.
    """
    to_process = data.groupby(["prompt_label", "shot", "model", "temperature"]).agg(
        precision_1_mean = ("precision@1", "mean"),
        precision_1_std = ("precision@1", "std"),
        BNPS_mean = ("BNPS", "mean"),
        BNPS_std = ("BNPS", "std"),
        false_positive_rate_mean =("false_positive_rate", "mean"),
        false_positive_rate_std = ("false_positive_rate", "std"),
        acc_top1_mean = ("acc_top1", "mean"),
        acc_top1_std = ("acc_top1", "std"),
        positional_similarity_mean = ("positional_similarity", "mean"),
        positional_similarity_std = ("positional_similarity", "std"),
        ndcg_standard_mean = ("ndcg_standard", "mean"),
        ndcg_standard_std = ("ndcg_standard", "std"),
        ndcg_inverted_mean =("ndcg_inverted", "mean"),
        ndcg_inverted_std = ("ndcg_inverted", "std"),
    )
    to_process["robust_BNPS"] = to_process["BNPS_mean"] - to_process["BNPS_std"]
    to_process.reset_index(inplace=True)
    return to_process.round(3)

def export_prompt_labels(data):
    """
    Exports 12 tables, one for each prompt label, shot pair. Rows contain model, temperature configs, while columns
    contain the 7 metrics.
    """
    grouped = data.groupby(["prompt_label", "shot"])
    for (prompt_label, shot), table in grouped:
        table["precision@1"] = table["precision_1_mean"].astype(str) + " +- " + table["precision_1_std"].astype(str)
        table["BNPS"] = table["BNPS_mean"].astype(str) + " +- " + table["BNPS_std"].astype(str)
        table["false_positive_rate"] = table["false_positive_rate_mean"].astype(str) + " +- " + table["false_positive_rate_std"].astype(str)
        table["acc_top1"] = table["acc_top1_mean"].astype(str) + " +- " + table["acc_top1_std"].astype(str)
        name = f"{prompt_label}_{shot}"
        name = re.sub(r"[\s+]+", "_", name)
        name = re.sub(r"_+", "_", name)
        table.drop(columns=["prompt_label", "shot", "precision_1_mean", "precision_1_std", "BNPS_mean", "BNPS_std",
                            "false_positive_rate_mean", "false_positive_rate_std", "acc_top1_mean", "acc_top1_std",
                            "positional_similarity_mean", "positional_similarity_std", "ndcg_standard_mean",
                            "ndcg_standard_std", "ndcg_inverted_mean", "ndcg_inverted_std"], inplace=True)
        table.to_csv(TABLES_DIR_PATH + f"/{name}.csv", index=False)


def plot_prompt_scores(data):
    """
        Conmputes prompt label, shot tables scores, considering model heuristic and top3 heuristic.
        Barplot prompt, shot tables (x = prompt + shot, y = model_heuristic, top3_heuristic)
        """
    model_heuristic = data.groupby(["prompt_label", "shot", "model"]).agg(
        model_score=("robust_BNPS", "max"),
    )
    model_heuristic = model_heuristic.groupby(["prompt_label", "shot"]).agg(
        model_score_heuristic=("model_score", "mean"),
    )
    top3 = data.groupby(["prompt_label", "shot"]).agg(
        top3_score_heuristic=("robust_BNPS", lambda x: x.sort_values(ascending=False).head(3).mean()),
    )
    model_heuristic.reset_index(inplace=True)
    top3.reset_index(inplace=True)
    scores = pd.merge(top3, model_heuristic, on=["prompt_label", "shot"])
    scores.set_index(["prompt_label", "shot"], inplace=True)

    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300

    ax = scores.plot.bar(figsize=(15, 10))
    plt.grid(True)
    plt.xticks(rotation=0)
    plt.title("Prompt Scores per each pair (prompt_label, shot_type)")
    plt.ylabel("Prompt Score")
    plt.xlabel("prompt, shot")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3, fontsize=6)
    labels = [textwrap.fill(label.get_text(), width=15) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0, fontsize=6)
    plt.rcParams['figure.dpi'] = 1000  # increases chart's resolution
    plt.ylim([0, 1])
    plt.savefig(os.path.join(PLOTS_PATH, "prompt_scores.png"))

def plot_prompt_trend(data):
    """
    Generates a boxplot chart for each prompt-shot pair.
    """
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    data.boxplot(column="BNPS", by=["prompt_label", "shot"], ax=ax, grid=True)
    ax.set_title("BNPS distribution per prompt/shot")
    ax.set_xlabel("prompt, shot")
    ax.set_ylabel("BNPS")
    labels = [textwrap.fill(label.get_text(), width=17) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0, fontsize=6)
    plt.xticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, "prompt_trends.png"))

def plot_temperature(data):
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    fig2, ax2 = plt.subplots(figsize=(15, 10), dpi=300)
    data = data.loc[(data["prompt_label"] == BEST_PROMPT) & (data["shot"] == BEST_SHOT)]
    grouped = data.groupby("model")
    for model, table in grouped:
        table.plot.line(x="temperature", ax=ax, y= "BNPS_mean", marker = "o", label = model)
        table.plot.line(x="temperature", ax=ax2, y= "BNPS_std", marker = "o", label = model)


    fig.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_mean.png"))
    fig2.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_std.png"))



if __name__ == "__main__":
    if not os.path.exists(AVG_RUNS_RESULTS_PATH):
        print(f"{AVG_RUNS_RESULTS_PATH} doesn't exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(AVG_RUNS_RESULTS_PATH):
        print(f"{AVG_RUNS_RESULTS_PATH} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(TABLES_DIR_PATH):
        print(f"{TABLES_DIR_PATH} doesn't exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(TABLES_DIR_PATH):
        print(f"{TABLES_DIR_PATH} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(PLOTS_PATH):
        print(f"{PLOTS_PATH} doesn't exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(PLOTS_PATH):
        print(f"{PLOTS_PATH} is not a directory", file=sys.stderr)
        sys.exit(1)

    df = load_runs()
    config_stats = compute_config_stats(df)
    export_prompt_labels(config_stats)
    plot_prompt_scores(config_stats)
    plot_prompt_trend(df)
    plot_temperature(config_stats)
