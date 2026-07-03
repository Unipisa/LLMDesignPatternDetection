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
- `data/ablation_analysis.py`: analysis and plotting utilities.
- `data/outputs/`: experimental outputs.
- `end_to_end_refactoring/`: controlled detector-to-refactorer case studies.

## Dataset

The dataset contains Python examples annotated with ranked lists of applicable design patterns.

The full dataset is split into:

- `data/config/validation_set.json`
- `data/config/test_set.json`

Each entry links a baseline implementation, one or more refactored versions, the associated tests, and the expected ranked pattern list.

## Running the Detector

The detector expects an OpenAI-compatible API endpoint. By default, it targets LM Studio at `http://127.0.0.1:1234/v1`.

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