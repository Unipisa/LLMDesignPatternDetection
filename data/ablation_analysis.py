import sys, os, re
import pandas as pd

from data.evaluate import false_positive_rate, positional_similarity

AVG_RUNS_RESULTS_PATH = "avg_results/runs_avg_results"
TABLES_DIR_PATH = "ablation/tables"

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
    grouped = data.groupby(["prompt_label", "shot"])
    for (prompt_label, shot), table in grouped:
        table["precision@1"] = table["precision_1_mean"].astype(str) + " +- " + table["precision_1_std"].astype(str)
        table["BNPS"] = table["BNPS_mean"].astype(str) + " += " + table["BNPS_std"].astype(str)
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

    df = load_runs()
    config_stats = compute_config_stats(df)
    export_prompt_labels(config_stats)