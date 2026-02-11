# evaluation/evaluate.py

import csv
import json
from collections import defaultdict

from evaluation.semantic import best_semantic_match
from evaluation.baseline import simple_baseline_question


# =============================
# Configuration
# =============================

BENCHMARK_PATH = "evaluation/benchmark.csv"
RESULTS_PATH = "outputs/latest_results.json"

SIM_THRESHOLD = 0.75


# =============================
# Utility Metrics
# =============================

def exact_match(pred: str, ground_truths: list) -> bool:
    return any(pred.strip().lower() == gt.strip().lower() for gt in ground_truths)


def jaccard_similarity(pred: str, gt: str) -> float:
    pred_tokens = set(pred.lower().split())
    gt_tokens = set(gt.lower().split())
    if not pred_tokens or not gt_tokens:
        return 0.0
    return len(pred_tokens & gt_tokens) / len(pred_tokens | gt_tokens)


def best_jaccard(pred: str, ground_truths: list) -> float:
    return max(jaccard_similarity(pred, gt) for gt in ground_truths)


# =============================
# Data Loading
# =============================

def load_benchmark(path: str):
    benchmark = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            benchmark[row["paper_id"]].append(row["ground_truth_question"])
    return benchmark


def load_predictions(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    predictions = defaultdict(list)
    for item in data:
        predictions[item["paper_id"]].append(item["question"])
    return predictions


# =============================
# Baseline Reconstruction
# =============================

def reconstruct_baseline_from_results(results_path: str):
    """
    Build baseline questions using existing signal excerpts
    stored in latest_results.json (no re-ingestion).
    """
    with open(results_path, encoding="utf-8") as f:
        data = json.load(f)

    baseline_predictions = defaultdict(list)

    for item in data:
        # reconstruct pseudo-signal
        signal = {
            "signal_type": item.get("signal_type", ""),
            "text_excerpt": item.get("question", "")
        }

        baseline_q = simple_baseline_question(signal)
        baseline_predictions[item["paper_id"]].append(baseline_q)

    return baseline_predictions


# =============================
# Core Evaluation
# =============================

def evaluate_system(predictions, benchmark):
    total_exact = 0
    total_jaccard = 0
    total_semantic = 0
    total_questions = 0
    total_semantic_matches = 0
    total_p_at_1 = 0
    total_papers = 0

    for paper_id, gt_questions in benchmark.items():
        pred_questions = predictions.get(paper_id, [])
        if not pred_questions:
            continue

        total_papers += 1

        for pred in pred_questions:
            total_questions += 1

            if exact_match(pred, gt_questions):
                total_exact += 1

            total_jaccard += best_jaccard(pred, gt_questions)

            best_sem = best_semantic_match(pred, gt_questions)
            total_semantic += best_sem

            if best_sem >= SIM_THRESHOLD:
                total_semantic_matches += 1

        # Precision@1 (semantic)
        top_pred = pred_questions[0]
        top_sim = best_semantic_match(top_pred, gt_questions)

        if top_sim >= SIM_THRESHOLD:
            total_p_at_1 += 1

    if total_questions == 0:
        return None

    return {
        "exact_match": total_exact / total_questions,
        "jaccard": total_jaccard / total_questions,
        "semantic_similarity": total_semantic / total_questions,
        "semantic_match_rate": total_semantic_matches / total_questions,
        "precision_at_1": total_p_at_1 / total_papers
    }


# =============================
# Main
# =============================

def evaluate():
    benchmark = load_benchmark(BENCHMARK_PATH)
    llm_predictions = load_predictions(RESULTS_PATH)
    baseline_predictions = reconstruct_baseline_from_results(RESULTS_PATH)

    llm_results = evaluate_system(llm_predictions, benchmark)
    baseline_results = evaluate_system(baseline_predictions, benchmark)

    print("\n==============================")
    print("V2 Evaluation Report")
    print("==============================")
    print(f"Semantic Threshold: {SIM_THRESHOLD}")
    print("------------------------------")

    print("\nLLM SYSTEM")
    for k, v in llm_results.items():
        print(f"{k.replace('_', ' ').title()}: {v:.3f}")

    print("\nBASELINE (Heuristic)")
    for k, v in baseline_results.items():
        print(f"{k.replace('_', ' ').title()}: {v:.3f}")

    print("==============================\n")


if __name__ == "__main__":
    evaluate()
