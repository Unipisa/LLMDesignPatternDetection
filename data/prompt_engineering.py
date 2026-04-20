from openai import OpenAI
import pandas as pd
import json
import os


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
            name = os.path.splitext(name)[0]    # remove extension
            name = name.replace("_baseline", "")    # removing naming convension
            gold_truth = example["pattern"]

            with open(path_baseline, "r") as g:
                code = g.read()
                response = client.chat.completions.create(
                    model=model_used,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": code}
                    ],
                    temperature=0.0,    # model response is now deterministic, no casuality

                    # uses structyured output (subset of json schema language)
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "design_pattern_response",
                            "strict": True,     # response MUST follow this response format
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "prediction": {"type": "array", "items": {"type": "string"},
                                                   "description": "Lista dei design pattern rilevati nel codice."}
                                },
                                "required": ["prediction"],
                                "additionalProperties": False
                            }
                        }
                    }
                )
                try:
                    ris = response.choices[0].message.content   # this is a string, not a dict ==> parsing with json
                    ris = json.loads(ris)
                    ris = ris["prediction"]
                except Exception as e:
                    print(f"Errore nel parsing del file {name}: {e}")
                    ris = ["ERRORE_PARSING"]

                df.loc[len(df)] = [id_example, name, prompt, gold_truth, ris, model_used]

        return df


if __name__ == "__main__":
    prompt_easy = ("Suggest the best design patterns appliable to refactor this code between abstract_factory, "
                   "factory_method, builder, command, strategy, template_method, state, proxy, decorator, adapter."
                   "Answer in JSON format, create a field 'prediction' with value the list of appliable design "
                   "patterns.")

    model_1 = "openai/gpt-oss-20b"

    output = start(prompt_easy, model_1)
    output.to_csv("output.csv", index=False)