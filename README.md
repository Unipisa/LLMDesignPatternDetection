# LLM Design Pattern Detection

Research prototype for recommending applicable GoF design patterns for Python code snippets using Large Language Models.

Given a baseline Python snippet, the detector queries an OpenAI-compatible LLM endpoint and returns a ranked list of candidate design patterns. Predictions are evaluated against a human-defined ranked ground truth.

## Repository Structure

- `data/baseline/`: baseline Python snippets.
- `data/refactored/`: corresponding refactored implementations.
- `data/tests_baseline/`: tests for baseline snippets.
- `data/tests_refactored/`: tests for refactored snippets.
- `data/config/`: dataset splits and prompt definitions.
- `data/detector.py`: LLM-based design pattern detector.
- `data/evaluate.py`: evaluation script.
- `data/outputs/`: experimental outputs.
- `end_to_end_refactoring/`: controlled detector-to-refactorer case studies.

## Dataset

The dataset contains Python examples annotated with ranked lists of applicable design patterns.

The full dataset is split into:

- `data/config/validation_set.json`
- `data/config/test_set.json`

Each entry links a baseline implementation, one or more refactored versions, the associated tests, and the expected ranked pattern list.

## Detector

`data/detector.py` queries an OpenAI-compatible LLM endpoint and saves the ranked design-pattern predictions for each baseline snippet.

It is used to generate the raw prediction files that are later evaluated.

Example:

```bash
cd data

python3 detector.py \
  --id 3 \
  --model openai/gpt-oss-20b \
  --one_shot \
  --temperature 0.0 \
  --dataset config/test_set.json \
  --output_dir outputs/test_set
```

By default, the detector expects LM Studio at:

```text
http://127.0.0.1:1234/v1
```

A different OpenAI-compatible endpoint can be used through `--base_url` and `--api_key`.

## Evaluation

`data/evaluate.py` reads prediction CSV files, computes ranking metrics against the ground truth, and writes evaluated outputs and aggregate summaries.

It is used to measure how well each model/prompt/temperature configuration performs.

For validation-style outputs organized under `results/original/run_*`:

```bash
cd data

python3 evaluate.py --experiment_dir outputs/validation_set
```

The evaluator computes:

- `hit_at_1`
- `BNPS`
- `false_positive_rate`
- `acc_top1`
- `positional_similarity`
- `ndcg_standard`
- `ndcg_inverted`

## End-to-End Pipeline

`end_to_end_refactoring/e2e_pipeline.py` runs the detector on controlled case-study examples and forwards valid predictions to a refactoring tool.

It is used to test whether detected design patterns can be consumed by a downstream refactoring pipeline.

Example:

```bash
python3 end_to_end_refactoring/e2e_pipeline.py
```

Before running it, update the `REFACTORER_PATH` constant inside:

```text
end_to_end_refactoring/e2e_pipeline.py
```

The path must point to the local `refactorer.py` file from the separate `LLMDesignPatternRefactoring` project.

That project is not vendored in this repository: the end-to-end pipeline assumes an external local checkout of `LLMDesignPatternRefactoring`, because the refactoring component belongs to a separate codebase.

## Refactorer Dependency

The end-to-end pipeline depends on the external refactoring tool provided by `LLMDesignPatternRefactoring`.

The expected setup is:

```text
LLMDesignPatternDetection/
LLMDesignPatternRefactoring/
```

Then configure `REFACTORER_PATH` accordingly, for example:

```python
REFACTORER_PATH = "/absolute/path/to/LLMDesignPatternRefactoring/refactorer.py"
```

The detector output is filtered against the case-study ground truth before invoking the refactorer. Therefore, the current end-to-end setup is controlled rather than fully autonomous.

## Analysis Utilities

`data/ablation_analysis.py` and the `data/ablation/` folder are only used for analysing the experimental results already produced by the detector and evaluator.

`end_to_end_refactoring/survey_analysis.py` is only used for analysing the survey responses collected for the controlled end-to-end case studies.

These analysis utilities are not required to run the detector, compute evaluation metrics, execute the end-to-end pipeline, or invoke the refactorer.

## Notes

This repository is a research artifact, not a packaged Python library.

Some runtime assumptions are local to the experimental setup, especially LM Studio and the external `LLMDesignPatternRefactoring` repository used by the end-to-end pipeline.
