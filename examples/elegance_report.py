#!/usr/bin/env python3
"""
Elegance reporting example for the Φ‑Generator.

This example monitors the elegance of the generator over multiple
evaluation cycles and saves a JSON report.
"""
import sys
import os
import json
import time

# Add parent directory to path for direct script execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiGenerator


def main():
    print("Φ‑Generator: Elegance Report")
    print("=" * 60)

    gen = PhiGenerator()
    gen.start()

    # Track elegance over time
    print("\nMonitoring elegance over 10 evaluation cycles...")
    print()
    print(f"{'Cycle':<8} {'Score (C/K)':<15} {'C':<12} {'K':<12} {'Entropy':<10}")
    print("-" * 65)

    history = []
    for cycle in range(10):
        metrics = gen.get_elegance(sample_size=500)
        history.append({
            "cycle": cycle,
            "score": metrics.score,
            "complexity": metrics.complexity,
            "consistency": metrics.consistency,
            "entropy": metrics.entropy_per_bit,
            "chi_square": metrics.chi_square,
            "autocorrelation": metrics.autocorrelation,
            "timestamp": metrics.timestamp,
        })
        print(
            f"{cycle:<8} "
            f"{metrics.score:<15.4f} "
            f"{metrics.complexity:<12.4f} "
            f"{metrics.consistency:<12.4f} "
            f"{metrics.entropy_per_bit:<10.4f}"
        )
        time.sleep(1)

    # Compute summary statistics
    scores = [entry["score"] for entry in history]
    best_score = min(scores)
    worst_score = max(scores)
    avg_score = sum(scores) / len(scores)

    # Save report
    report = {
        "generator": "Φ‑Generator",
        "version": "1.0.0",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
        "summary": {
            "best_score": best_score,
            "worst_score": worst_score,
            "avg_score": avg_score,
            "evaluation_count": len(history),
        },
        "elegance_history": history,
        "final_status": gen.get_status(),
    }
    report_path = "elegance_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nSummary:")
    print(f"  Best:  {best_score:.4f}")
    print(f"  Worst: {worst_score:.4f}")
    print(f"  Avg:   {avg_score:.4f}")
    print(f"\nReport saved to {report_path}")

    gen.stop()
    print("\nΦ")


if __name__ == '__main__':
    main()
