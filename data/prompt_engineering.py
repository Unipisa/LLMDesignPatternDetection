from openai import OpenAI
import pandas as pd
import json
import os
import argparse
import subprocess
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


# noinspection PyTypeChecker
def start(prompt_used: str, model_used: str, url: str, key : str, label_used: str,  tem: float, one_shot: bool = False):
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
                    temperature=tem,
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
    parser.add_argument("--one_shot", action= "store_true", help= "Model will receive a pair of example-answer to help solving the task")
    parser.add_argument("--temperature", type=float, help= "Temperature to use for the model", required= True)
    parser.add_argument("--run_id", type=int, required=True, help="Run id to create output dir")

    args = parser.parse_args()
    prompts = json.load(open("config/prompts.json", "r"))
    prompt = prompts[args.id]["prompt"]
    label = prompts[args.id]["label"]
    run_id = args.run_id

    local = (args.base_url == "http://127.0.0.1:1234/v1") and (args.api_key == "lm-studio")
    output = None
    try:
        if local:
            print("Starting lm studio server...")
            subprocess.run("lms server start", shell=True)  # launches <lms server start> command on shell

        print(f"Starting shot: {args.model}")
        output = start(prompt, args.model, args.base_url, args.api_key, label, args.temperature, args.one_shot)  # this is a pandas.Dataframe object
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


    if args.one_shot:
        shot = "one-shot"
    else:
        shot = "zero-shot"

    model_safe = args.model.split("/")[-1]

    if not os.path.exists(f"results/original/run_{run_id}"):
        os.makedirs(f"results/original/run_{run_id}", exist_ok=True)

    output.to_csv(f"results/original/run_{run_id}/{model_safe}_{shot}_id{args.id}_temp{args.temperature}.csv", index=False)
