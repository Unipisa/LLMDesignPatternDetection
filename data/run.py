import subprocess
import time


MODELS = ["qwen/qwen3.5-9b", "openai/gpt-oss-20b", "google/gemma-4-e4b"]

def f():
    for i in range(3):
        for model in MODELS:
            for one_shot in [True, False]:
                flag = "--one_shot" if one_shot else ""
                subprocess.run(f"python3 prompt_engineering.py --id {i} --model '{model}' {flag}", shell=True)
                time.sleep(20)


if __name__ == "__main__":
    f()