#!/usr/bin/env python3
"""PolEval 2026 Task 3: evaluate public surrogate authorship classifiers.

Usage:
  python evaluate_authorship.py --input public_dev.json
  python evaluate_authorship.py --input transformed.json --label-map label_map.json

Input JSON: a list of objects containing `text` and `author`, or an object
with a `data`, `examples`, `records`, or `items` list. A transformed submission
must retain the original author labels to calculate classification metrics.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODELS = {
    "roberta_base": "Ewel/PolEval2026-Task3-Authorship-RoBERTa-Base",
    "roberta_large": "Ewel/PolEval2026-Task3-Authorship-RoBERTa-Large",
}


def load_records(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in ("data", "examples", "records", "items"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list) or not data:
        raise ValueError("Input must be a non-empty JSON list of records.")
    for i, row in enumerate(data):
        if not isinstance(row, dict) or not isinstance(row.get("text"), str) or not row["text"].strip():
            raise ValueError(f"Record {i} must contain nonempty string field 'text'.")
        if not isinstance(row.get("author"), str) or not row["author"].strip():
            raise ValueError(f"Record {i} must contain nonempty string field 'author'.")
    return data


def read_label_map(path):
    if path is None:
        return None
    with open(path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    if not isinstance(mapping, dict):
        raise ValueError("Label map must be a JSON object: {author_name: class_id}.")
    return {str(name): int(idx) for name, idx in mapping.items()}


def resolve_mapping(config, authors, override):
    id2label = {int(k): str(v) for k, v in config.id2label.items()}
    num_labels = config.num_labels
    if override is not None:
        mapping = override
    else:
        mapping = {name: idx for idx, name in id2label.items()}
        if not set(authors).issubset(mapping):
            labels = ", ".join(f"{k}: {v}" for k, v in sorted(id2label.items()))
            raise ValueError(
                "Cannot safely map authors to model class IDs. "
                f"Model id2label = [{labels}]. "
                "Supply --label-map label_map.json with the EXACT mapping used "
                "during training, e.g. {\"Author name\": 0, ...}. "
                "Do not assume alphabetical order."
            )
    if any(name not in mapping for name in authors):
        raise ValueError(f"Missing authors in label map: {sorted(set(authors) - set(mapping))}")
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("Label map must map each author to a distinct class ID.")
    if any(idx < 0 or idx >= num_labels for idx in mapping.values()):
        raise ValueError(f"Class IDs must be between 0 and {num_labels - 1}.")
    return mapping


def run_model(model_name, repo, records, args, override):
    print(f"\n{'=' * 76}\nMODEL: {model_name} ({repo})\n{'=' * 76}", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(repo)
    model = AutoModelForSequenceClassification.from_pretrained(repo)
    model.to("cpu")
    model.eval()

    authors = sorted({row["author"] for row in records})
    mapping = resolve_mapping(model.config, authors, override)
    print("Author → class ID:", mapping, flush=True)
    texts = [row["text"] for row in records]
    y_true = np.asarray([mapping[row["author"]] for row in records], dtype=int)
    y_pred_parts = []
    prob_parts = []

    with torch.inference_mode():
        for start in range(0, len(texts), args.batch_size):
            batch = texts[start:start + args.batch_size]
            tokens = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=args.max_length,
                return_tensors="pt",
            )
            logits = model(**tokens).logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            prob_parts.append(probs)
            y_pred_parts.append(probs.argmax(axis=-1))
            if not args.quiet:
                print(f"Processed {min(start + len(batch), len(texts))}/{len(texts)}", end="\r", flush=True)
    if not args.quiet:
        print()

    y_pred = np.concatenate(y_pred_parts)
    probabilities = np.concatenate(prob_parts)
    labels = list(range(model.config.num_labels))
    reverse_map = {idx: name for name, idx in mapping.items()}
    names = [reverse_map.get(idx, str(model.config.id2label.get(idx, f"class_{idx}"))) for idx in labels]
    report = classification_report(
        y_true, y_pred, labels=labels, target_names=names, digits=4, zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print("\nClassification report:\n", report)
    print("Confusion matrix (rows=true, columns=predicted):")
    print("Class order:", names)
    print(matrix)

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        output = []
        for i, row in enumerate(records):
            output.append({
                "index": i,
                "author": row["author"],
                "predicted_author": reverse_map.get(int(y_pred[i]), names[int(y_pred[i])]),
                "predicted_class_id": int(y_pred[i]),
                "probabilities": {names[j]: float(probabilities[i, j]) for j in labels},
            })
        (out_dir / f"{model_name}_predictions.json").write_text(
            json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (out_dir / f"{model_name}_report.txt").write_text(
            f"Model: {repo}\nMapping: {mapping}\nAccuracy: {accuracy_score(y_true, y_pred):.4f}\n\n"
            f"{report}\nConfusion matrix:\n{matrix}\n",
            encoding="utf-8",
        )
        print(f"Saved results in: {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="PolEval 2026 Task 3 public authorship evaluation (CPU).")
    parser.add_argument("--input", required=True, help="Path to JSON with 'text' and 'author' fields")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--label-map", default=None, help="JSON mapping author name to model class ID")
    parser.add_argument("--output-dir", default=None, help="Optional directory for predictions/reports")
    parser.add_argument("--models", nargs="+", choices=list(MODELS), default=list(MODELS))
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.batch_size <= 0 or args.max_length <= 0:
        parser.error("--batch-size and --max-length must be positive")
    torch.set_num_threads(min(4, torch.get_num_threads()))
    records = load_records(args.input)
    override = read_label_map(args.label_map)
    print(f"Examples: {len(records)}; authors: {sorted(set(row['author'] for row in records))}")
    for name in args.models:
        run_model(name, MODELS[name], records, args, override)


if __name__ == "__main__":
    main()
