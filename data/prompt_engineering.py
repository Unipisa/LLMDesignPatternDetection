from openai import OpenAI
import pandas as pd
import json
import os
import argparse


# noinspection PyTypeChecker
def start(prompt: str, model_used: str):
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

    df = pd.DataFrame(columns=["id", "prompt", "model", "name_baseline", "gold_truth", "prediction"])

    with open("training_set.json", "r") as f:
        training_set = json.load(f)
        for example in training_set:
            path_baseline = example["path_baseline"]
            id_example = example["id"]
            name = os.path.basename(path_baseline)
            name = os.path.splitext(name)[0]  # remove extension
            name = name.replace("_baseline", "")  # removing naming convension
            gold_truth = example["pattern"]

            with open(path_baseline, "r") as g:
                code = g.read()
                response = client.chat.completions.create(
                    model=model_used,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": code}
                    ],
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
                    ris = json.loads(ris)
                    ris = ris["prediction"]
                except Exception as e:
                    print(f"Errore nel parsing del file {name}: {e}")
                    ris = ["ERRORE_PARSING"]

                df.loc[len(df)] = [id_example, prompt, model_used, name, gold_truth, ris]

        return df

def evaluate(df: pd.DataFrame):
    for idx, row in df.iterrows():
        gold_truth = row["gold_truth"]
        prediction = row["prediction"]
        if isinstance(gold_truth, str):
            gold_truth = eval(gold_truth)  # parsing string to list
        if isinstance(prediction, str):
            prediction = eval(prediction)

        truth_set = set(gold_truth)
        pred_set = set(prediction)
        tp = len(truth_set.intersection(pred_set))

        acc_top1 = 1 if gold_truth[0] in pred_set else 0
        jaccard = tp / len(truth_set | pred_set) if (truth_set | pred_set) else 0
        precision = tp / len(pred_set) if pred_set else 0
        recall = tp / len(truth_set) if truth_set else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

        df.loc[idx, "acc_top1"] = round(acc_top1, 3)
        df.loc[idx, "jaccard"] = round(jaccard, 3)
        df.loc[idx, "precision"] = round(precision, 3)
        df.loc[idx, "recall"] = round(recall, 3)
        df.loc[idx, "f1"] = round(f1, 3)
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, help="ID of the prompt to use")
    args = parser.parse_args()
    prompts = json.load(open("prompts.json", "r"))
    prompt = prompts[args.id]["prompt"]
    model = prompts[args.id]["model"]
    output = start(prompt, model)
    evaluate(output)

    metrics = ["acc_top1", "jaccard", "precision", "recall", "f1"]
    summary = output[metrics].mean().to_dict()      # mean of all valuation metrics
    prompts[args.id]["acc_top1"] = round (summary["acc_top1"], 3) # round to 3 decimal places
    prompts[args.id]["jaccard"] = round(summary["jaccard"], 3)
    prompts[args.id]["precision"] = round(summary["precision"], 3)
    prompts[args.id]["recall"] = round(summary["recall"], 3)
    prompts[args.id]["f1"] = round(summary["f1"], 3)

    output.to_csv(prompts[args.id]["csv_path"], index=False)

    # save updated prompts.json with metrics
    with open("prompts.json", "w") as f:
        json.dump(prompts, f, indent=4)
