import sys
import argparse
import pandas as pd
import json
import os

def ndcg(prediction: list, ground_truth: list, k: int = None) -> float:
    if k:
        prediction = prediction[:k]

    # 1 if predicted design pattern in ground_truth, 0 otherwise
    gains = [1 if p in set(ground_truth) else 0 for p in prediction]

    # DCG: weighted sum by position
    dcg = sum(g / (i + 1) for i, g in enumerate(gains))

    # IDCG: ideal case (all relevant design patterns in top positions)
    ideal = sorted(gains, reverse=True)
    idcg = sum(g / (i + 1) for i, g in enumerate(ideal))

    return dcg / idcg if idcg > 0 else 0.0

def positional_similarity(list1, list2):
    len_max = max(len(list1), len(list2))
    return sum([1 if a == b else 0 for a, b in zip(list1, list2)])/ len_max if len_max > 0 else 0


# Metric to penalize pattern "spamming" (model returns all patterns): 1.0 if model spams
def false_positive_rate(prediction: list, ground_truth: list) -> float:
    all_patterns = ["abstract_factory", "factory_method", "builder", "command", "strategy", "template_method", "state",
                    "proxy", "decorator", "adapter"]
    possible_wrong_patterns = set(all_patterns) - set(ground_truth)
    wrong_patterns = set(prediction) - set(ground_truth)    # false positives: patterns predicted as relevant but not in ground_truth
    return len(wrong_patterns) / len(possible_wrong_patterns) if possible_wrong_patterns else 0.0


def evaluate(df: pd.DataFrame):
    for idx, row in df.iterrows():
        ground_truth = row["ground_truth"]
        prediction = row["prediction"]
        if isinstance(ground_truth, str):
            ground_truth = eval(ground_truth)  # parsing string to list
        if isinstance(prediction, str):
            prediction = eval(prediction)

        hit_at_1 = 1 if prediction[0] in ground_truth else 0
        top_1 = 1 if prediction[0] == ground_truth[0] else 0
        ndcg_standard = ndcg(prediction, ground_truth)
        ndcg_inverted = ndcg(ground_truth, prediction)
        pos_similarity = positional_similarity(ground_truth, prediction)
        bnps = (ndcg_standard + ndcg_inverted + pos_similarity) / 3

        df.loc[idx, "hit_at_1"] = round(hit_at_1, 3)
        df.loc[idx, "BNPS"] = round(bnps, 3)
        df.loc[idx, "false_positive_rate"] = round(false_positive_rate(prediction, ground_truth), 3)
        df.loc[idx, "acc_top1"] = round(top_1, 3)
        df.loc[idx, "positional_similarity"] = round(pos_similarity, 3)
        df.loc[idx, "ndcg_standard"] = round(ndcg_standard, 3)
        df.loc[idx, "ndcg_inverted"] = round(ndcg_inverted, 3)


def extract_configuration (filename):
    basename = os.path.basename(filename)

    # Rimuove l'estensione .csv
    name_without_extension = os.path.splitext(basename)[0]

    # Effettua lo split partendo da destra per massimo 3 volte
    # Formato atteso: modello_shot_idX_tempY
    fields = name_without_extension.split("_")
    if len(fields) != 4:
        print(f"File {filename} has wrong format", file=sys.stderr)
        return None, None, None, None

    # Assegnazione e pulizia dei prefissi "id" e "temp"
    model = fields[0]
    shot = fields[1]

    with open("config/prompts.json", "r") as f:
        prompts = json.load(f)
    id_prompt = int(fields[2].replace("id", ""))
    prompt_label = prompts[id_prompt]["label"]
    temperature = float(fields[3].replace("temp", ""))

    return model, shot, prompt_label, temperature


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_dir", type=str, default=".", help="Experiment directory")
    args = parser.parse_args()
    ris_path = os.path.join(args.experiment_dir, "results", "original")
    output_path = os.path.join(args.experiment_dir, "results", "evaluated")
    avg_path = os.path.join(args.experiment_dir, "avg_results")

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(avg_path, "runs_avg_results"), exist_ok=True)


    metrics = ["hit_at_1", "BNPS", "false_positive_rate", "acc_top1", "positional_similarity",
               "ndcg_standard", "ndcg_inverted"]
    results = []
    for directory in os.listdir(ris_path):
        rows = []
        if not os.path.isdir(os.path.join(ris_path, directory)):
            print(f"File {directory} is not a directory", file=sys.stderr)
            continue
        if not os.access(os.path.join(ris_path, directory), os.X_OK) or not os.access(os.path.join(ris_path, directory), os.R_OK):
            print(f"Cannot access directory {os.path.join(ris_path, directory)}", file=sys.stderr)
            continue
        for file in os.listdir(f"{ris_path}/{directory}"):
            if file.endswith(".csv"):
                to_process = pd.read_csv(f"{ris_path}/{directory}/{file}")
                evaluate(to_process)
                if not os.path.exists(f"{output_path}/{directory}"):
                    # Sostituisci le righe 84-85 con:
                    os.makedirs(f"{output_path}/{directory}", exist_ok=True)
                to_process.to_csv(f"{output_path}/{directory}/{file}", index=False)
                summary = to_process[metrics].mean().to_dict()  # mean of all valuation metrics
                for metric in metrics:
                    summary[metric] = round(summary[metric], 3)

                model, shot, prompt_label, temperature = extract_configuration(file)
                if model is None:
                    continue

                summary["model"] = model
                summary["shot"] = shot
                summary["prompt_label"] = prompt_label
                summary["temperature"] = temperature
                rows.append(summary)

        if len(rows) == 0:
            print(f"File {directory} is empty", file=sys.stderr)
            continue

        df = pd.DataFrame(rows)[["model", "shot", "prompt_label", "temperature", "hit_at_1", "BNPS",
                                 "false_positive_rate", "acc_top1", "positional_similarity", "ndcg_standard",
                                 "ndcg_inverted" ]]

        if not os.path.exists(f"{avg_path}"):
            os.makedirs(f"{avg_path}", exist_ok=True)
        df.to_csv(f"{avg_path}/runs_avg_results/{directory}_avg_results.csv", index=False)
        results.append(df)

    combined = pd.concat(results, ignore_index=True)
    total_summary = (combined.groupby(["model", "shot", "prompt_label", "temperature"])[metrics]
                     .mean().round(3).reset_index())

    total_summary.to_csv(f"{avg_path}/total_avg_results.csv", index=False)


