# LLM Design Pattern Detection

Research prototype for recommending applicable GoF design patterns for Python code snippets using Large Language Models. The detector returns a ranked list of candidate patterns, evaluated against a manually defined ranked ground truth. A controlled toolchain connects the detector to a separate refactoring tool.

## Setup

Use **Python 3.12 or newer**, as required by some dataset examples. Run the commands below from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

This installs the detector, analysis and test dependencies. Live model inference also requires LM Studio and a compatible local model, or another OpenAI-compatible endpoint. Analysing the stored results does not require a running LLM.

## Dataset and repository structure

The dataset contains **31 Python examples**, split into **21 validation examples** and **10 test examples**. Each entry provides a baseline implementation, corresponding refactored versions, unit tests and a ranked list of applicable design patterns.

| Location | Contents |
|---|---|
| `data/config/` | Full dataset metadata, validation/test splits and prompt definitions |
| `data/dataset/baseline/` | Baseline implementations |
| `data/dataset/refactored/` | Reference refactored implementations |
| `data/dataset/tests_baseline/`, `data/dataset/tests_refactored/` | Dataset unit tests |
| `data/detector/detector.py` | Design pattern recommender |
| `data/detector/evaluate.py` | Ranking metrics and validation-run evaluation |
| `data/detector/ablation/` | Analysis script, figures and exported tables |
| `data/random_baseline_generator.py` | Frequency-weighted random recommender |
| `data/end_to_end_refactoring/` | Controlled case studies, toolchain and survey analysis |

## Results by research question

| Research question | Results |
|---|---|
| **RQ1 — Design pattern detection** | Predictions, evaluated validation runs and aggregate scores in `data/detector/results/validation_set/`; test predictions and aggregate scores in `data/detector/results/test_set/`; random-reference results in `data/detector/results/random_baseline/`. Figures and tables are in `data/detector/ablation/`. |
| **RQ2 — Design pattern refactoring** | Maintained in the separate [LLMDesignPatternRefactoring repository](https://github.com/Unipisa/LLMDesignPatternRefactoring). |
| **RQ3 — Overall toolchain** | Detector outputs and generated refactorings in `data/end_to_end_refactoring/results/`; case-study inputs in `examples/`; responses in `survey_results.csv`; stored survey figures in `survey/`, all under `data/end_to_end_refactoring/`. |

## Run the detector

The default endpoint is LM Studio at `http://127.0.0.1:1234/v1`. The default local execution starts the server and attempts to unload the selected model and stop the server afterwards. The `lms` command must be available on your PATH.

```bash
python3 data/detector/detector.py \
  --id 3 \
  --model openai/gpt-oss-20b \
  --one_shot \
  --temperature 0.0 \
  --dataset data/config/test_set.json \
  --output_dir data/detector/results/test_set
```

Use an identifier available in your LM Studio installation for `--model`. `--id` selects a prompt from `data/config/prompts.json`; omitting `--one_shot` selects zero-shot prompting. The command processes every example in the supplied dataset JSON and writes a prediction CSV to `--output_dir`.

Use `--skip_lmstudio_management` when the local server and model are already managed separately. For another OpenAI-compatible endpoint, pass `--base_url` and `--api_key`.

## Evaluate predictions

The evaluator computes `hit_at_1`, `BNPS`, `false_positive_rate`, `acc_top1`, `positional_similarity`, `ndcg_standard` and `ndcg_inverted`.

For validation runs arranged as `results/original/run_*/<model>_<shot>_id<N>_temp<T>.csv`, run:

```bash
python3 data/detector/evaluate.py \
  --experiment_dir data/detector/results/validation_set
```

Within the experiment directory, it writes evaluated CSVs to `results/evaluated/`, per-run summaries to `avg_results/runs_avg_results/`, and the overall summary to `avg_results/total_avg_results.csv`.

This CLI expects the run-directory structure above. To evaluate an individual CSV, including a test prediction file or the random reference, import `evaluate` as shown below. The function adds metric columns to the supplied DataFrame; save it explicitly to retain the results.

## Frequency-weighted random reference

Generate one prediction per test example:

```bash
python3 data/random_baseline_generator.py --seed 42
```

Pattern frequencies are estimated from validation ground truths only. Each test prediction samples distinct patterns sequentially without replacement, weighted by these frequencies. Its length equals the corresponding test ground truth length, so the reference has access to the correct list length. The seed makes the generation reproducible; this is one sampled list per example, not an average over repeated random generations.

Evaluate and save the predictions by running this Python code from the repository root:

```python
import pandas as pd
from data.detector.evaluate import evaluate

folder = "data/detector/results/random_baseline"
results = pd.read_csv(f"{folder}/random_weighted_predictions.csv")
evaluate(results)
results.to_csv(f"{folder}/random_weighted_evaluated.csv", index=False)
print(results["BNPS"].mean())
```

The test-set comparison plot reads `random_weighted_evaluated.csv` and draws its mean BNPS as a horizontal reference. Generate and evaluate this file before regenerating the ablation figures if it is not already present. These steps make no LLM calls.

## Regenerate figures and tables

The scripts analyse stored data and overwrite generated files with matching names:

```bash
python3 data/detector/ablation/ablation_analysis.py
python3 data/end_to_end_refactoring/survey_analysis.py
```

- **Ablation:** reads the detector's validation/test results and evaluated random reference. Saves figures to `data/detector/ablation/plots/` and tables to `data/detector/ablation/tables/`.
- **Survey:** reads `data/end_to_end_refactoring/survey_results.csv`. Saves regenerated figures to `data/end_to_end_refactoring/plots/`; the existing `survey/` folder contains stored figures.

Both scripts resolve their data paths from their own location and create output directories if necessary. Copy the required PDFs into the manuscript project separately.

## Run the controlled toolchain

`data/end_to_end_refactoring/toolchain.py` runs the detector on the case-study dataset and forwards predictions that belong to each example's ground truth to the refactorer. This filtering makes the experiment controlled rather than fully autonomous.

The refactorer is an external dependency. Install its dependencies according to its own README and keep the checkouts side by side:

```text
LLMDesignPatternDetection/
LLMDesignPatternRefactoring/
```

By default, `REFACTORER_PATH` in `toolchain.py` points to the sibling project's `refactorer.py`. Update that constant if your checkout is elsewhere. The script currently uses `openai/gpt-oss-20b`, prompt ID 3, one-shot prompting and temperature 0.0; ensure the model is available locally or update the model identifiers in the script.

```bash
python3 data/end_to_end_refactoring/toolchain.py
```

The toolchain starts and stops the LM Studio server and invokes the refactorer with the same Python interpreter. Results are written under `data/end_to_end_refactoring/results/detector/` and `data/end_to_end_refactoring/results/refactorer/`.

## Tests

Run the dataset and case-study tests from the repository root:

```bash
python3 -m pytest
```

These tests do not require live LLM calls. This repository is a research artifact rather than a packaged Python library.
