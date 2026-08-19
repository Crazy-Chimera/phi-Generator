#!/usr/bin/env python3
"""
Basic usage example for the Φ‑Generator.

This example demonstrates all core functionality:
- Single random value
- Uniform distribution
- Normal distribution
- Exponential distribution
- Elegance metrics
"""
import sys
import os

# Add parent directory to path for direct script execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiGenerator


def main():
    print("Φ‑Generator: Basic Usage")
    print("=" * 60)

    # Create and start the generator
    gen = PhiGenerator()
    gen.start()

    # 1. Generate a single random value
    value = gen.random()
    print(f"\n1. Single uniform sample in [0, 1]:")
    print(f"   {value:.6f}")

    # 2. Generate uniform samples
    samples = gen.uniform(10, 20, n=5)
    print(f"\n2. Five uniform samples in [10, 20]:")
    for i, s in enumerate(samples, 1):
        print(f"   {i}: {s:.6f}")

    # 3. Generate normal samples
    samples = gen.normal(mean=100, std=15, n=5)
    print(f"\n3. Five normal samples (μ=100, σ=15):")
    for i, s in enumerate(samples, 1):
        print(f"   {i}: {s:.6f}")

    # 4. Generate exponential samples
    samples = gen.exponential(rate=0.5, n=5)
    print(f"\n4. Five exponential samples (λ=0.5):")
    for i, s in enumerate(samples, 1):
        print(f"   {i}: {s:.6f}")

    # 5. Get elegance metrics
    metrics = gen.get_elegance()
    print(f"\n5. Elegance metrics:")
    print(f"   Score (C/K):      {metrics.score:.4f}")
    print(f"   Complexity (C):   {metrics.complexity:.4f}")
    print(f"   Consistency (K):  {metrics.consistency:.4f}")
    print(f"   Entropy per bit:  {metrics.entropy_per_bit:.4f}")
    print(f"   Chi‑square:       {metrics.chi_square:.6f}")
    print(f"   Autocorrelation:  {metrics.autocorrelation:.6f}")

    gen.stop()
    print("\nΦ")


if __name__ == '__main__':
    main()
