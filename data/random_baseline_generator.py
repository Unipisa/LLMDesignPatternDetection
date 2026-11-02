#!/usr/bin/env python3
"""Genera predizioni random pesate, senza chiamate LLM o dipendenze esterne."""
import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validation', type=Path, default=repo / 'data/config/validation_set.json')
    parser.add_argument('--test', type=Path, default=repo / 'data/config/test_set.json')
    parser.add_argument('--output', type=Path, default=repo / 'data/detector/results/random_baseline/random_weighted_predictions.csv')
    parser.add_argument('--seed', type=int, default=42, help='Facoltativo: rende riproducibile il campionamento')
    args = parser.parse_args()
    with open(args.validation, 'r') as f:
        validation = json.load(f)
    with open(args.test, 'r') as f:
        test = json.load(f)
    if not validation or not test:
        parser.error('Validation e test non possono essere vuoti')
    if {e['id'] for e in validation} & {e['id'] for e in test}:
        parser.error('Validation e test devono avere ID disgiunti')
    for entry in validation + test:
        patterns = entry['pattern']
        if not patterns or len(patterns) != len(set(patterns)):
            parser.error(f"Ground truth vuota o duplicata per ID {entry['id']}")

    total = sum(len(entry["pattern"]) for entry in validation)  # total number of patterns
    unique_patterns = {p for entry in validation for p in entry['pattern']}
    counts = {
        p: sum(p in entry['pattern'] for entry in validation)
        for p in unique_patterns
    }
    rng = random.Random(args.seed)
    rows = []
    for entry in test:
        truth = entry['pattern']
        remaining = sorted(counts)
        if len(truth) > len(remaining):
            parser.error('Pattern con peso positivo insufficienti per la lunghezza richiesta')
        prediction = []
        for _ in range(len(truth)):
            # choices normalizza automaticamente i pesi dei candidati rimasti.
            chosen = rng.choices(remaining, weights=[counts[p] for p in remaining], k=1)[0]
            prediction.append(chosen)
            remaining.remove(chosen)
        rows.append({
            'id': entry['id'],
            'prompt_used': 'random weighted by validation frequency; ground-truth length',
            'model': 'random-weighted',
            'name_baseline': Path(entry['path_baseline']).stem,
            'ground_truth': json.dumps(truth),
            'prediction': json.dumps(prediction),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Distribuzione stimata dal validation:')
    for pattern, count in counts.items():
        print(f'  {pattern}: {count / total:.4%}')
    print(f'\nSalvate {len(rows)} predizioni in {args.output.resolve()}')
    print(f'Seed: {args.seed!r} (None = nuova casualita a ogni esecuzione)')


if __name__ == '__main__':
    main()


# Probability estimated on validation set, comparison on test set