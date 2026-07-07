import subprocess
from pathlib import Path
import pandas as pd
import os
import ast
import json
import requests

DETECTOR_TO_REFACTORER = {
    "strategy": "strategy",
    "factory_method": "factorymethod",
    "template_method": "template_method",
    "decorator": "decorator",
    "adapter": "adapter",
    "state": "state",
}

REFACTORER_PATH = "/Users/alessandrofiumano/Documents/LLMDesignPatternRefactoring/refactorer.py"
REFACTORER_ROOT = Path(REFACTORER_PATH).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]

def unload_model(model_name: str):
    url = "http://127.0.0.1:1234/api/v1/models/unload"
    payload = {"instance_id": model_name}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"Model {model_name} unloaded successfully")
    else:
        print(f"Failed to unload model {model_name}: {response.text}")
        exit(1)

def launch_detector():
    cmd = [
        "python",
        "detector.py",
        "--id", "3",
        "--model", "openai/gpt-oss-20b", 
        "--one_shot",
        "--temperature", "0.0",
        "--dataset", "data/end_to_end_refactoring/e2e_dataset.json",
        "--output_dir", "data/end_to_end_refactoring/results/detector",
        "--skip_lmstudio_management"
    ]
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)

def launch_refactorer(df):
    with open(REPO_ROOT / "data/end_to_end_refactoring/e2e_dataset.json", "r") as f:
        dataset = json.load(f)

    examples_by_id = {example["id"]: example for example in dataset}

    for _, row in df.iterrows():
        example = examples_by_id[int(row["id"])]

        predictions = row["prediction"]
        if isinstance(predictions, str):
            predictions = ast.literal_eval(predictions)

        patterns_to_process = [pattern for pattern in predictions if pattern in example["pattern"]]

        for pattern in patterns_to_process:
            pattern_index = example["pattern"].index(pattern)
            refactorer_pattern = DETECTOR_TO_REFACTORER.get(pattern)

            if refactorer_pattern is None:
                continue

            code_path = os.path.join(REPO_ROOT, example["path_baseline"])
            test_refactored = os.path.join(REPO_ROOT, example["tests_refactored"][pattern_index])
            save_folder = os.path.join(REPO_ROOT, "data/end_to_end_refactoring/results/refactorer")

            cmd = [
                "python",
                REFACTORER_PATH,
                str(code_path),
                str(test_refactored),
                refactorer_pattern,
                str(save_folder),
                "--strategy", "lmstudio",
                "--model_name", "openai/gpt-oss-20b",
                "--temperature", "0.0",
            ]

            subprocess.run(cmd, check=True, cwd=REFACTORER_ROOT)

if __name__ == "__main__":
    try:
        subprocess.run("lms server start", shell=True, check=True)
        launch_detector()
        detector_dir = os.path.join(REPO_ROOT, "data/end_to_end_refactoring/results/detector")
        detector_csv = None
        for file in os.listdir(detector_dir):
            if file.endswith(".csv"):
                detector_csv = os.path.join(detector_dir, file)
                break

        if detector_csv is None:
            exit(1)
        detector_output = pd.read_csv(detector_csv)
        launch_refactorer(detector_output)
    finally:
        unload_model("openai/gpt-oss-20b")
        subprocess.run("lms server stop", shell=True)
