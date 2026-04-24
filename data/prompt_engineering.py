from openai import OpenAI
import pandas as pd
import json
import os
import argparse
import subprocess
import time
import requests


EXAMPLE = """
class DocDataMiner:
    def mine(self, path):
        file = open(path, "rb")
        raw = file.read()
        data = raw.decode().split("\n")          # parse DOC
        analysis = {"righe": len(data), "parole": sum(len(r.split()) for r in data)}
        print(analysis)
        file.close()

class CSVDataMiner:
    def mine(self, path):
        file = open(path, "rb")
        raw = file.read()
        lines = raw.decode().split("\n")
        h = lines[0].split(",")
        data = [dict(zip(h, r.split(","))) for r in lines[1:] if r]  # parse CSV
        analysis = {"righe": len(data), "parole": sum(len(str(r).split()) for r in data)}
        print(analysis)
        file.close()

class PDFDataMiner:
    def mine(self, path):
        file = open(path, "rb")
        raw = file.read()
        data = [r for r in raw.decode("latin-1").split("\n") if r.strip()]  # parse PDF
        analysis = {"righe": len(data), "parole": sum(len(r.split()) for r in data)}
        print(analysis)
        file.close()
"""

ANSWER = '{"prediction": ["template_method", "strategy", "proxy"]}'

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


# Metrics to penalize pattern "spamming" (model returns all patterns)
def precision(prediction: list, ground_truth: list) -> float:
    relevant_retrieved = len(set(prediction) & set(ground_truth))
    return relevant_retrieved / len(set(prediction)) if prediction else 0.0

def jaccard_similarity(prediction: list, ground_truth: list) -> float:
    # len(intersection) / len(union)
    set_pred = set(prediction)
    set_gt = set(ground_truth)
    intersection = len(set_pred & set_gt)
    union = len(set_pred | set_gt)
    return intersection / union if union else 0.0

# noinspection PyTypeChecker
def start(prompt_used: str, model_used: str, url: str, key : str, label_used: str, one_shot: bool = False):
    client = OpenAI(base_url = url, api_key = key)

    df = pd.DataFrame(columns=["id", "prompt_used", "model", "name_baseline", "ground_truth", "prediction"])

    with open("config/training_set.json", "r") as f:
        training_set = json.load(f)
        for example in training_set:
            path_baseline = example["path_baseline"]
            id_example = example["id"]
            name = os.path.basename(path_baseline)
            name = os.path.splitext(name)[0]  # remove extension
            name = name.replace("_baseline", "")  # removing naming convension
            ground_truth = example["pattern"]

            with open(path_baseline, "r") as g:
                code = g.read()

                msg = [{"role": "system", "content": prompt_used}]
                if one_shot:
                    msg.append({"role": "user", "content": EXAMPLE})
                    msg.append({"role": "assistant", "content": ANSWER})
                msg.append({"role": "user", "content": code})

                response = client.chat.completions.create(
                    model=model_used,
                    messages=msg,
                    temperature=0.3,
                    seed=42,  # trying to get equal responses from different executionts

                    # uses structyured output (subset of json schema language)
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "design_pattern_response",
                            "strict": True,  # response MUST follow this response format
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "prediction": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": [
                                                 "abstract_factory",
                                                 "factory_method",
                                                 "builder",
                                                 "command",
                                                 "strategy",
                                                 "template_method",
                                                 "state",
                                                 "proxy",
                                                 "decorator",
                                                 "adapter"
                                            ]
                                        },
                                        "minItems": 1,
                                        "uniqueItems": True,
                                    "description": "List of design patterns detected in the code."
                                    }
                                },
                                "required": ["prediction"],
                                "additionalProperties": False
                            }
                        }
                    }
                )
                try:
                    ris = response.choices[0].message.content  # this is a string, not a dict ==> parsing with json
                    if not ris:  # fallback per thinking models (es. Qwen)
                        ris = response.choices[0].message.model_extra.get("reasoning_content", "")
                    ris = json.loads(ris)
                    ris = ris["prediction"]
                except Exception as e:
                    print(f"Errore nel parsing del file {name}: {e}")
                    ris = ["ERRORE_PARSING"]

                df.loc[len(df)] = [id_example, label_used, model_used, name, ground_truth, ris]

        return df

def evaluate(df: pd.DataFrame):
    for idx, row in df.iterrows():
        ground_truth = row["ground_truth"]
        prediction = row["prediction"]
        if isinstance(ground_truth, str):
            ground_truth = eval(ground_truth)  # parsing string to list
        if isinstance(prediction, str):
            prediction = eval(prediction)

        acc_top1 = 1 if prediction[0] in ground_truth else 0

        df.loc[idx, "acc_top1"] = round(acc_top1, 3)
        df.loc[idx, "ndcg"] = round(ndcg(prediction, ground_truth), 3)
        df.loc[idx, "ndcg@3"] = round(ndcg(prediction, ground_truth, k=3), 3)
        df.loc[idx, "precision"] = round(precision(prediction, ground_truth), 3)
        df.loc[idx, "jaccard"] = round(jaccard_similarity(prediction, ground_truth), 3)



def unload_model(model_name: str):
    url = "http://127.0.0.1:1234/api/v1/models/unload"
    payload = {"instance_id": model_name}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"Model {model_name} unloaded successfully")
    else:
        print(f"Failed to unload model {model_name}: {response.text}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, help="ID of the prompt_used to use")
    parser.add_argument("--model", type=str, required=True, help="Model to use")
    parser.add_argument("--base_url", type=str, default="http://127.0.0.1:1234/v1", help="Base URL per OpenAI API")
    parser.add_argument("--api_key", type=str, default="lm-studio", help="API key per OpenAI API")
    parser.add_argument("--one_shot", action= "store_true", help= "Model will receive a pair of example-answer to help solving the"
                                                                      " task")
    args = parser.parse_args()
    prompts = json.load(open("config/prompts.json", "r"))
    prompt = prompts[args.id]["prompt"]
    label = prompts[args.id]["label"]

    local = (args.base_url == "http://127.0.0.1:1234/v1") and (args.api_key == "lm-studio")
    output = None
    try:
        if local:
            print("Starting lm studio server...")
            subprocess.run("lms server start", shell=True)  # launches <lms server start> command on shell
            time.sleep(5)  # Wait 5 seconds to make sure server is runnig

        print(f"Starting shot: {args.model}")
        output = start(prompt, args.model, args.base_url, args.api_key, label, args.one_shot)  # this is a pandas.Dataframe object
        print("Shot completed: ", args.model)
    finally:
        if local:
            # unloads all uploaded models and stops server
            unload_model(args.model)
            print("Stopping lm studio server...")
            subprocess.run("lms server stop", shell=True)

    if output is None:
        print("No output from OpenAI API")
        exit(1)


    evaluate(output)

    metrics = ["acc_top1", "ndcg", "ndcg@3", "precision", "jaccard"]
    summary = output[metrics].mean().to_dict()      # mean of all valuation metrics
    summary["acc_top1"] = round(summary["acc_top1"], 3) # round to 3 decimal places
    summary["ndcg"] = round(summary["ndcg"], 3)
    summary["ndcg@3"] = round(summary["ndcg@3"], 3)
    summary["precision"] = round(summary["precision"], 3)
    summary["jaccard"] = round(summary["jaccard"], 3)

    if args.one_shot:
        shot = "one_shot"
    else:
        shot = "zero_shot"

    model_safe = args.model.split("/")[-1]
    output.to_csv(f"prompt_results/{shot}/prompt_{model_safe}_{args.id}.csv", index=False)

    # saving "summary" of this execution
    with open(f"config/results.json", "r") as f:
        data = json.load(f)

    data.setdefault(model_safe, {}).setdefault(shot, {})[label] = {       # creates keys if they don't exist', updates otherwise
        "acc_top1": summary["acc_top1"],
        "ndcg": summary["ndcg"],
        "ndcg@3": summary["ndcg@3"],
        "precision": summary["precision"],
        "jaccard": summary["jaccard"]
    }

    with open(f"config/results.json", "w") as f:
        json.dump(data, f, indent=4)
