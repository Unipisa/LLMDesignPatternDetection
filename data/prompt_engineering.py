from openai import OpenAI
import pandas as pd
import json
import os
import argparse


# noinspection PyTypeChecker
def start(prompt: str, model_used: str):
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

    df = pd.DataFrame(columns=["id", "name_baseline", "prompt", "gold_truth", "prediction", "model"])

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

                df.loc[len(df)] = [id_example, name, prompt, gold_truth, ris, model_used]

        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, help="ID of the prompt to use")
    prompts = json.load(open("prompts.json", "r"))
    prompt = prompts[parser.parse_args().id]["prompt"]
    model = prompts[parser.parse_args().id]["model"]
    output = start(prompt, model)
    output.to_csv(prompts[parser.parse_args().id]["csv_path"], index=False)
