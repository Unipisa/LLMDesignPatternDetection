import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
import os
import textwrap
import seaborn as sns

CSV_PATH = "/Users/alessandrofiumano/Downloads/survey_results.csv"
PLOTS_PATH = "/Users/alessandrofiumano/Documents/OverleafThesis/figures/survery_plots"


DIMENSIONS = [
    "Behaviour preservation",
    "Design pattern consistency",
    "Refactoring quality",
    "Readability and maintainability",
    "Absence of evident issues",
]

CASES = [
    "SecureCommunicator (Strategy)",
    "MediaStreaming (Strategy)",
    "MediaStreaming (Factory Method)",
    "PaymentProcessor (Strategy)",
    "PaymentProcessor (Decorator)",
]

EDU_COL     = "What is the highest level of education you have completed?"
YOE_COL     = "How many years of programming experience do you have (YoE)?"
SUCCESS_COL = "How would you rate the overall success of the refactorings presented in this survey?"
USEFUL_COL  = "How would you rate the usefulness of the system that produced the refactorings presented in this survey?"


def find_col(df, prefix):
    """Trova la prima colonna il cui nome inizia con `prefix` (strip + case-insensitive)."""
    prefix_low = prefix.strip().lower()
    for c in df.columns:
        if c.strip().lower().startswith(prefix_low):
            return c
    return None


def load_data(path=CSV_PATH):
    df = pd.read_csv(path)
    df = df.rename(columns=lambda col: col.split(":", 1)[0].strip())
    df = df.rename(columns=lambda col: col.replace("consistency-", "consistency -"))
    df = df.rename(columns={df.columns[0]: "Timestamp"})
    return df

def get_ratings(df):
    """Restituisce solo le colonne numeriche di rating."""
    skip_prefixes = ("Timestamp", EDU_COL, YOE_COL, SUCCESS_COL, USEFUL_COL, "Comments")
    cols = [c for c in df.columns
            if not any(c.startswith(p) for p in skip_prefixes)
            and "Comments" not in c]
    return df[cols].apply(pd.to_numeric, errors="coerce")


def plot_demographics(df):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    for ax, col, title in zip(axes,
                               [EDU_COL, YOE_COL],
                               ["Education Level", "Years of Experience"]):
        counts = df[col].value_counts()
        ax.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.0f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 14}
        )

    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "participant_demographics.pdf"), bbox_inches="tight")



def plot_heatmap(df):
    ratings = get_ratings(df)
    matrix = []
    for case in CASES:
        row = []
        for dim in DIMENSIONS:
            prefix = f"{dim} - {case}"
            col = find_col(ratings, prefix)
            row.append(ratings[col].mean() if col else np.nan)
        matrix.append(row)

    data = np.array(matrix, dtype=float)
    dim_labels = [textwrap.fill(d, width=13) for d in DIMENSIONS]
    case_labels = [textwrap.fill(case, width=16) for case in CASES]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        data,
        ax=ax,
        annot=True,
        annot_kws={"fontsize": 12},
        fmt=".2f",
        cmap="viridis",
        vmin=1,
        vmax=5,
        xticklabels=dim_labels,
        yticklabels=case_labels,
     )
    ax.tick_params(axis="x", labelsize=14, rotation=0)
    ax.tick_params(axis="y", labelsize=14, rotation=0)
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "mean_rating_per_case_study.pdf"), bbox_inches="tight")


def plot_boxplots_per_case(df):
    ratings = get_ratings(df)
    data_per_case = pd.DataFrame({
        case: ratings.filter(like=case).stack().reset_index(drop=True)
        for case in CASES
    })

    fig, ax = plt.subplots(figsize=(11, 5))
    data_per_case.boxplot(ax=ax, grid=True)

    ax.set_xticks(range(1, len(CASES) + 1))
    wrapped_cases = [textwrap.fill(case, width=18) for case in CASES]
    ax.set_xticklabels(wrapped_cases, rotation=0, fontsize=13)
    ax.set_ylim(0.5, 5.5)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.tick_params(axis="y", labelsize=13, pad=8)
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "rating_distribution_per_case_study.pdf"), bbox_inches="tight")


def plot_overall_ratings(df):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    for ax, col, title in zip(axes,
                               [SUCCESS_COL, USEFUL_COL],
                               ["Overall Refactoring Success", "Usefulness of the System"]):
        counts = df[col].value_counts().sort_index()
        ax.pie(counts.values, labels=counts.index, autopct="%1.0f%%",
               startangle=90,
               wedgeprops={"edgecolor": "white", "linewidth": 2},
               textprops={"fontsize": 14}
               )

    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_PATH, "overall_judgements.pdf"), bbox_inches="tight")


if __name__ == "__main__":
    df = load_data()
    if df.empty:
        print("No responses yet — populate the CSV and re-run.")
        sys.exit(1)
    plot_demographics(df)
    plot_heatmap(df)
    plot_boxplots_per_case(df)
    plot_overall_ratings(df)
