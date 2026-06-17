import sys, os, re
import textwrap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import seaborn as sns

from data.evaluate import false_positive_rate, positional_similarity

AVG_RUNS_RESULTS_PATH = "outputs/validation_set/avg_results/runs_avg_results"
TABLES_DIR_PATH = "ablation/tables"
AVG_TEST_RESULTS_PATH = "outputs/test_set/test_set_avg_results.csv"
AVG_VALIDATION_RESULTS_PATH = "outputs/validation_set/avg_results/total_avg_results.csv"

# stable configuration
PLOTS_PATH = "ablation/plots"
BEST_PROMPT = "role + base + output description + rules"
BEST_SHOT = "one-shot"
BEST_TEMPERATURE = 0.0

# configuration with best performance, without considering std
OPTIMAL_PROMPT = "improved by chatGPT"
OPTIMAL_SHOT = "zero-shot"
OPTIMAL_TEMPERATURE = 0.0
OPTIMAL_MODEL = "gemma-4-e4b"

METRICS = ["hit_at_1", "BNPS", "false_positive_rate"]
MODELS = ["gemma-4-e4b", "gpt-oss-20b", "qwen3.5-9b"]

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
    """
    to_process = data.groupby(["prompt_label", "shot", "model", "temperature"]).agg(
        BNPS_mean = ("BNPS", "mean"),
        BNPS_std = ("BNPS", "std"),
        false_positive_rate_mean =("false_positive_rate", "mean"),
        false_positive_rate_std = ("false_positive_rate", "std"),
        hit_at_1_mean = ("hit_at_1", "mean"),
        hit_at_1_std = ("hit_at_1", "std"),
        acc_top1_mean = ("acc_top1", "mean"),
        acc_top1_std = ("acc_top1", "std"),
        positional_similarity_mean = ("positional_similarity", "mean"),
        positional_similarity_std = ("positional_similarity", "std"),
        ndcg_standard_mean = ("ndcg_standard", "mean"),
        ndcg_standard_std = ("ndcg_standard", "std"),
        ndcg_inverted_mean =("ndcg_inverted", "mean"),
        ndcg_inverted_std = ("ndcg_inverted", "std"),
    )
    to_process.reset_index(inplace=True)
    return to_process.round(3)

def export_prompt_labels(data):
    """
    Exports 12 tables, one for each prompt label, shot pair. Rows contain model, temperature configs, while columns
    contain the 7 metrics.
    """
    grouped = data.groupby(["prompt_label", "shot"])
    for (prompt_label, shot), table in grouped:
        table["BNPS"] = table["BNPS_mean"].astype(str) + " ± " + table["BNPS_std"].astype(str)
        table["false_positive_rate"] = table["false_positive_rate_mean"].astype(str) + " ± " + table["false_positive_rate_std"].astype(str)
        table["hit_at_1"] = table["hit_at_1_mean"].astype(str) + " ± " + table["hit_at_1_std"].astype(str)
        table["acc_top1"] = table["acc_top1_mean"].astype(str) + " ± " + table["acc_top1_std"].astype(str)
        table["positional_similarity"] = table["positional_similarity_mean"].astype(str) + " ± " + table["positional_similarity_std"].astype(str)
        table["ndcg_standard"] = table["ndcg_standard_mean"].astype(str) + " ± " + table["ndcg_standard_std"].astype(str)
        table["ndcg_inverted"] = table["ndcg_inverted_mean"].astype(str) + " ± " + table["ndcg_inverted_std"].astype(str)
        name = f"{prompt_label}_{shot}"
        name = re.sub(r"[\s+]+", "_", name)
        name = re.sub(r"_+", "_", name)
        table.drop(columns=["prompt_label", "shot", "hit_at_1_mean", "hit_at_1_std", "BNPS_mean", "BNPS_std",
                            "false_positive_rate_mean", "false_positive_rate_std", "acc_top1_mean", "acc_top1_std",
                            "positional_similarity_mean", "positional_similarity_std", "ndcg_standard_mean",
                            "ndcg_standard_std", "ndcg_inverted_mean", "ndcg_inverted_std"], inplace=True)
        table.to_csv(TABLES_DIR_PATH + f"/{name}.csv", index=False)



def plot_prompt_plots(data):
    """
    Generates a chart for each prompt-shot pair, considering BNPS, hit_at_1 and false-positive rate.
    """
    for metric in ["BNPS", "false_positive_rate"]:
        fig, ax = plt.subplots(figsize=(18, 6))
        data.boxplot(column=metric, by=["prompt_label", "shot"], ax=ax, grid=True)
        fig.suptitle("")
        ax.set_xlabel("prompt, shot")
        ax.set_ylabel(metric)
        labels = [textwrap.fill(label.get_text(), width=17) for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels, rotation=0, fontsize=6)
        plt.xticks(rotation=0, fontsize=8)
        plt.tight_layout()
        ax.set_title(f"{metric} distribution by prompt-shot configuration")
        plt.savefig(os.path.join(PLOTS_PATH, f"prompt_boxplot_{metric}.pdf"))

    for metric in ["acc_top1", "hit_at_1"]:
        grouped = data.groupby(["prompt_label", "shot"])[metric].agg(["mean", "std"])
        fig, ax = plt.subplots(figsize=(18, 6))
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
        plt.savefig(os.path.join(PLOTS_PATH, f"prompt_barplot_{metric}.pdf"))

def plot_temperature_avg(data):
    """
    Description
    """
    models = sorted(data["model"].unique())
    fig, axes = plt.subplots(
        1,
        len(models),
        figsize=(18, 6),
        sharey=True
    )
    avg_by_model_temperature = data.groupby(["model", "shot", "temperature"]).agg(
        BNPS_mean=("BNPS", "mean"),
        BNPS_std=("BNPS", "std"),
        false_positive_rate_mean=("false_positive_rate", "mean"),
        false_positive_rate_std=("false_positive_rate", "std")
    )
    avg_by_model_temperature.reset_index(inplace=True)
    shot_colors = dict(zip(
        sorted(avg_by_model_temperature["shot"].unique()),
        plt.rcParams["axes.prop_cycle"].by_key()["color"]
    ))
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
                    linestyle="--" if metric == "false_positive_rate_mean" else "-",
                    color=shot_colors[shot],
                    label = f"{metric} ({shot})",
                )
                ax.grid(True)
                ax.set_xlabel("temperature")
                ax.set_title(model)

    fig.suptitle("Average BNPS and false-positive rate over all prompt configurations by temperature and shot", fontsize=16)
    plt.legend(loc="best")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, f"avg_temperature_performance.pdf"))


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
    fig.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_best.pdf"))

    # LINE PLOT FOR OPTIMAL PROMPT
    data2 = data.loc[(data["prompt_label"] == OPTIMAL_PROMPT) & (data["shot"] == OPTIMAL_SHOT)]
    fig2, axes2 = plt.subplots(
        1,
        len(models),
        figsize=(18, 6),
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
    fig2.savefig(os.path.join(PLOTS_PATH, "temperature_BNPS_optimal.pdf"))

def temperature_boxolpot (data):
    """
    Generates a boxplot chart for each temperature.
    """
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(18, 6),
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
    plt.savefig(os.path.join(PLOTS_PATH, "temperature_boxplots.pdf"))

def model_barplot(data):
    data = data.loc[
        (data["prompt_label"] == BEST_PROMPT)
        & (data["shot"] == BEST_SHOT)
        & (data["temperature"] == BEST_TEMPERATURE)
    ]
    fig, ax = plt.subplots(figsize=(18, 6))
    data.plot.bar(x="model",
                  y=["BNPS_mean", "false_positive_rate_mean", "hit_at_1_mean"],
                  figsize=(18, 6),
                  grid=True,
                  ax=ax
                  )
    ax.set_yticks(np.arange(0, 1.01, 0.1))
    ax.legend(loc="best")
    ax.set_title(f"Model performance considering prompt {BEST_PROMPT} ({BEST_SHOT}) and T = {BEST_TEMPERATURE}")
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "model_barplots_prompt_stable.pdf"))

def plot_design_patterns_performance():
    """
    Creates heatmap on design patterns considering the selected configurations (ablation end). This function averages
    metric values across runs and does not report standard deviation.
    """
    with open("config/prompts.json", "r") as f:
        prompts = json.load(f)
    prompt_label_to_id = {p["label"]: p["id"] for p in prompts}
    prompt_id_to_label = {p["id"]: p["label"] for p in prompts}

    with open("config/validation_set.json", "r") as f:
        validation_set = json.load(f)
        id_to_category = {item["id"]: item["category"] for item in validation_set}

    best_confs = [f"{model}_{BEST_SHOT}_id{prompt_label_to_id[BEST_PROMPT]}_temp{BEST_TEMPERATURE}" for model in MODELS]
    best_confs.append(f"{OPTIMAL_MODEL}_{OPTIMAL_SHOT}_id{prompt_label_to_id[OPTIMAL_PROMPT]}_temp{OPTIMAL_TEMPERATURE}")
    for metric in METRICS:
        metric_series = []
        for best_conf in best_confs:
            # average results extraction for each conf.
            base_dir = "outputs/validation_set/results/evaluated"
            run_dirs = [d for d in os.listdir(base_dir) if d.startswith("run_")
                        and os.path.isfile(os.path.join(base_dir, d,  best_conf+".csv"))]
            if not run_dirs:
                print(f"No run found for {best_conf}", file=sys.stderr)
                continue
            frames = []
            for run_dir in run_dirs:
                tmp = pd.read_csv(os.path.join(base_dir, run_dir, best_conf+".csv"))
                tmp["id"] = tmp["id"].astype(int)
                frames.append(tmp)
            df_runs = pd.concat(frames)
            df_runs ["category"] = df_runs["id"].map(id_to_category)
            metric_by_pattern = df_runs.groupby("category")[metric].mean().reindex(["behavioural", "creational", "structural"])

            metric_by_pattern.name = best_conf
            metric_series.append(metric_by_pattern)

        # plotting
        df_metric = pd.concat(metric_series, axis=1).T  # index contains the selected configurations
        readable_labels = []
        for conf in df_metric.index:
            model, rest = conf.split("_", 1)
            shot, rest = rest.split("_id", 1)
            prompt_id, temperature = rest.split("_temp", 1)
            prompt_label = prompt_id_to_label[int(prompt_id)]
            label = f"{prompt_label} ({shot}), T={temperature}, {model}"
            readable_labels.append(textwrap.fill(label, width=30))
        df_metric.index = readable_labels

        fig, ax = plt.subplots(figsize=(18, 6))
        cmap = "viridis_r" if metric == "false_positive_rate" else "viridis"
        sns.heatmap(
            df_metric,
            ax=ax,
            annot=True,
            fmt=".3f",
            vmin=0,
            vmax=1,
            cmap=cmap
        )

        # colorbar label
        colorbar = ax.collections[0].colorbar
        colorbar.set_label("")

        if metric == "false_positive_rate":
            # Lower values are better
            arrow_start = (4, 0.95)
            arrow_end = (4, 0.05)
            better_y = 0.03
            worse_y = 0.97
        else:
            # Higher values are better
            arrow_start = (4, 0.05)
            arrow_end = (4, 0.95)
            better_y = 0.97
            worse_y = 0.03

        colorbar.ax.annotate(
            "",
            xy=arrow_end,
            xytext=arrow_start,
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", lw=2.5, color="black"),
            clip_on=False,
        )
        colorbar.ax.text(4, better_y, "Better", transform=colorbar.ax.transAxes,
                         ha="center", va="center", fontsize=10)
        colorbar.ax.text(4, worse_y, "Worse", transform=colorbar.ax.transAxes,
                         ha="center", va="center", fontsize=10)



        ax.set_xlabel("Category")
        ax.set_title(f"Average {metric} per design pattern category across selected configurations", pad =30)

        plt.tight_layout()
        output_path = f"{PLOTS_PATH}/design-patterns-performance-by_{metric}.pdf"
        plt.savefig(output_path)

def end_ablation_study():
    validation = pd.read_csv(AVG_VALIDATION_RESULTS_PATH)
    test = pd.read_csv(AVG_TEST_RESULTS_PATH)
    validation = validation.loc[((validation["prompt_label"] == BEST_PROMPT) & (validation["shot"] == BEST_SHOT) & (validation["temperature"] == BEST_TEMPERATURE))|
                                ((validation["prompt_label"] == OPTIMAL_PROMPT) & (validation["temperature"] == OPTIMAL_TEMPERATURE) & (validation["shot"] == OPTIMAL_SHOT))]

    test = test.loc[((test["prompt_label"] == BEST_PROMPT) & (test["shot"] == BEST_SHOT) & (test["temperature"] == BEST_TEMPERATURE)) |
                    ((test["prompt_label"] == OPTIMAL_PROMPT) & (test["shot"] == OPTIMAL_SHOT)) & (test["temperature"] == OPTIMAL_TEMPERATURE)]

    validation["config"] = validation["prompt_label"] + "\nshot=" + validation["shot"].astype(str) + " t=" + validation["temperature"].astype(str)
    test["config"] = test["prompt_label"] + "\nshot=" + test["shot"].astype(str) + " t=" + test["temperature"].astype(str)

    validation = validation.pivot(index="config", columns="model", values="BNPS")
    test = test.pivot(index="config", columns="model", values="BNPS")


    fig1, ax1 = plt.subplots(figsize=(18, 6))
    fig2, ax2 = plt.subplots(figsize=(18, 6))
    validation.plot.bar(title="BNPS performance on validation set considering the best and optimal configurations", figsize=(18, 6), grid=True, ax=ax1)
    output_path_validation = f"{PLOTS_PATH}/stable-optimal-bnps-validation.pdf"
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis="x", labelrotation=0)
    for container in ax1.containers:
        ax1.bar_label(container, fmt="%.3f")
    fig1.tight_layout()

    test.plot.bar(title="BNPS performance on test set considering the best and optimal configurations", figsize=(18, 6), grid=True, ax=ax2)
    output_path_test = f"{PLOTS_PATH}/stable-optimal-bnps-test.pdf"
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis="x", labelrotation=0)
    for container in ax2.containers:
        ax2.bar_label(container, fmt="%.3f")
    fig2.tight_layout()

    fig1.savefig(output_path_validation)
    fig2.savefig(output_path_test)


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
    model_barplot(config_stats)
    plot_design_patterns_performance()
    end_ablation_study()
