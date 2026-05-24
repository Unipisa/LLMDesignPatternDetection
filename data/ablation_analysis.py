import sys, os, re
import textwrap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data.evaluate import false_positive_rate, positional_similarity

AVG_RUNS_RESULTS_PATH = "avg_results/runs_avg_results"
TABLES_DIR_PATH = "ablation/tables"

# stable configuration
PLOTS_PATH = "ablation/plots"
BEST_PROMPT = "role + base + output description + rules"
BEST_SHOT = "one-shot"
BEST_TEMPERATURE = 0.0
BEST_MODEL = None

# configuration with best performance, without considering std
OPTIMAL_PROMPT = "improved by chatGPT"
OPTIMAL_SHOT = "zero-shot"
OPTIMAL_TEMPERATURE = 0.0
OPTIMAL_MODEL = "gemma-4-e4b"

METRICS = ["precision@1", "BNPS", "false_positive_rate"]

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



def plot_prompt_plots(data):
    """
    Generates a chart for each prompt-shot pair, considering BNPS, precision@1 and false-positive rate.
    """
    for metric in ["BNPS", "false_positive_rate"]:
        fig, ax = plt.subplots(figsize=(18, 6), dpi=300)
        data.boxplot(column=metric, by=["prompt_label", "shot"], ax=ax, grid=True)
        fig.suptitle("")
        ax.set_xlabel("prompt, shot")
        ax.set_ylabel(metric)
        labels = [textwrap.fill(label.get_text(), width=17) for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels, rotation=0, fontsize=6)
        plt.xticks(rotation=0, fontsize=8)
        plt.tight_layout()
        ax.set_title(f"{metric} distribution by prompt-shot configuration")
        plt.savefig(os.path.join(PLOTS_PATH, f"prompt_boxplot_{metric}.png"))

    for metric in ["acc_top1", "precision@1"]:
        grouped = data.groupby(["prompt_label", "shot"])[metric].agg(["mean", "std"])
        fig, ax = plt.subplots(figsize=(18, 6), dpi=300)
        grouped["mean"].plot.bar(yerr=grouped["std"], ax=ax, capsize=5)
        labels = [textwrap.fill(label.get_text(), width=17) for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels, rotation=0, fontsize=6)
        plt.xticks(rotation=0, fontsize=8)
        ax.set_xlabel("prompt, shot")
        plt.title(f"Average {metric} over all prompts")
        ax.set_ylabel(metric)
        ax.set_yticks(np.arange(0, 1.01, 0.1))
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_PATH, f"prompt_barplot_{metric}.png"))

def plot_temperature_avg(data):
    """
    Description
    """
    models = sorted(data["model"].unique())
    fig, axes = plt.subplots(
        1,
        len(models),
        figsize=(18, 6),
        dpi=300,
        sharey=True
    )
    avg_by_model_temperature = data.groupby(["model", "shot", "temperature"]).agg(
        BNPS_mean=("BNPS", "mean"),
        BNPS_std=("BNPS", "std"),
        false_positive_rate_mean=("false_positive_rate", "mean"),
        false_positive_rate_std=("false_positive_rate", "std")
    )
    avg_by_model_temperature.reset_index(inplace=True)
    for metric, std in zip(["BNPS_mean", "false_positive_rate_mean"], ["BNPS_std", "false_positive_rate_std"]):
        for ax, model in zip(axes, models):
            table = avg_by_model_temperature.loc[avg_by_model_temperature["model"] == model].sort_values("temperature")
            for shot, table in table.groupby("shot"):
                ax.errorbar(
                    table["temperature"],
                    table[metric],
                    yerr=table[std],
                    capsize=5,
                    marker="o",
                    label = f"{metric} ({shot})",
                )
                ax.grid(True)
                ax.set_xlabel("temperature")
                ax.set_title(model)

    fig.suptitle("Average BNPS and false-positive rate over all prompt configurations by temperature and shot", fontsize=16)
    plt.legend(loc="best")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, f"avg_temperature_performance.png"))


def plot_temperature_lineplot(data):
    """
    Generates a line plot for each model considering two of bests prompts (x temperature, y BNPS)
    """

    # LINE PLOT FOR BEST PROMPT
    data1 = data.loc[(data["prompt_label"] == BEST_PROMPT) & (data["shot"] == BEST_SHOT)]
    models = sorted(data["model"].unique())
    fig, axes = plt.subplots(
        1,
        len(models),
        figsize=(18, 6),
        dpi=300,
        sharey=True
    )
    for ax, model in zip(axes, models):
        table = data1.loc[data1["model"] == model].sort_values("temperature")
        ax.errorbar(
            table["temperature"],
            table["BNPS_mean"],
            yerr=table["BNPS_std"],
            marker="o",
            capsize=5,
            linewidth=2,
            elinewidth=1.2,
            alpha=0.85,
            label=model,
        )
        ax.grid(True, alpha=0.4)
        ax.set_title(model)
        ax.set_xlabel("temperature")
    axes[0].set_ylabel("BNPS_mean", labelpad=18)
    fig.suptitle(f"BNPS mean ± std: {BEST_PROMPT} ({BEST_SHOT})")
    axes[0].set_ylim(0.4, 0.75)
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_best.png"))

    # LINE PLOT FOR OPTIMAL PROMPT
    data2 = data.loc[(data["prompt_label"] == OPTIMAL_PROMPT) & (data["shot"] == OPTIMAL_SHOT)]
    fig2, axes2 = plt.subplots(
        1,
        len(models),
        figsize=(18, 6),
        dpi=300,
        sharey=True
    )
    for ax, model in zip(axes2, models):
        table = data2.loc[data2["model"] == model].sort_values("temperature")
        ax.errorbar(
            table["temperature"],
            table["BNPS_mean"],
            yerr=table["BNPS_std"],
            marker="o",
            capsize=5,
            linewidth=2,
            elinewidth=1.2,
            alpha=0.85,
            label=model,
        )
        ax.grid(True, alpha=0.4)
        ax.set_title(model)
        ax.set_xlabel("temperature")
    axes2[0].set_ylabel("BNPS_mean", labelpad=18)
    fig2.suptitle(f"BNPS mean ± std: {OPTIMAL_PROMPT} ({OPTIMAL_SHOT})")
    axes2[0].set_ylim(0.4, 0.75)
    plt.tight_layout()
    fig2.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_optimal.png"))

def temperature_boxolpot (data):
    """
    Generates a boxplot chart for each temperature.
    """
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(18, 6),
        dpi=300,
        sharey=True
    )
    for ax, (prompt, shot) in zip(axes, zip([BEST_PROMPT, OPTIMAL_PROMPT], [BEST_SHOT, OPTIMAL_SHOT])):
        table = data.loc[(data["prompt_label"] == prompt) & (data["shot"] == shot)]
        table.boxplot(column="BNPS", by="temperature", ax=ax, grid=True)
        ax.set_title(f"{prompt}, {shot}")
        ax.set_xlabel("temperature")
        labels = [textwrap.fill(label.get_text(), width=17) for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels, rotation=0, fontsize=6)
        plt.xticks(rotation=0, fontsize=8)

    fig.suptitle("BNPS distribution by temperature for selected prompt-shot configurations")
    axes[0].set_ylabel("BNPS")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, "temperature_boxplots.png"))


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
    plot_prompt_plots(df)
    plot_temperature_avg(df)
    plot_temperature_lineplot(config_stats)
    temperature_boxolpot(df)
