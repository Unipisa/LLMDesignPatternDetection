import sys

import pandas as pd
import matplotlib.pyplot as plt
import os
import textwrap


"""
Calcola tutti i plot necessari salvandoli dove opportuno
"""

def plot_prompt_performance(df):
    to_plot = df.groupby("prompt_label").agg(
        avg_precision_1 = ("precision@1", "mean"),
        avg_bnps = ("BNPS", "mean"),
        avg_false_positive_rate = ("false_positive_rate", "mean"),
        avg_acc_top1 = ("acc_top1", "mean"),
        avg_positional_similarity = ("positional_similarity", "mean"),
        avg_ndcg_standard = ("ndcg_standard", "mean"),
        avg_ndcg_inverted = ("ndcg_inverted", "mean")
    )
    to_plot = to_plot.T
    ax = to_plot.plot.bar(figsize=(15, 10))
    labels = [textwrap.fill(label.get_text(), width=15) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0)
    plt.yticks([i/10 for i in range(0, 12, 2)])
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3, rotation=90)

    ax.legend(loc='best', fontsize='small')
    plt.title("Average performance per prompt", y=0.75)
    plt.rcParams['figure.dpi'] = 300    # increases chart's resolution
    output_path = "plots/prompt_performance.png"
    plt.tight_layout()
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
        ax.bar_label(container, fmt="%.2f", padding=3)
    plt.tight_layout()
    ax.legend(loc='best', fontsize='small')
    plt.title("Average model-shot performance", y=0.95)
    plt.rcParams['figure.dpi'] = 300  # increases chart's resolution
    output_path = "plots/model-shot_performance.png"
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