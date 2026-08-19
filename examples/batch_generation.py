#!/usr/bin/env python3
"""
Batch generation example for the Φ‑Generator.

This example demonstrates high‑throughput generation of large batches
and basic statistical properties of the output.
"""
import sys
import os
import time

# Add parent directory to path for direct script execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiGenerator


def main():
    print("Φ‑Generator: Batch Generation")
    print("=" * 60)

    gen = PhiGenerator()
    gen.start()

    # Generate a large batch of uniform samples
    print("\nGenerating 100,000 uniform samples...")
    start = time.time()
    samples = gen.uniform(0, 1, n=100_000)
    elapsed = time.time() - start
    print(f"Generated {len(samples)} samples in {elapsed:.2f} seconds")
    print(f"Throughput: {len(samples) / elapsed:.0f} samples/second")

    # Compute basic statistics
    mean = sum(samples) / len(samples)
    variance = sum((s - mean) ** 2 for s in samples) / len(samples)
    print(f"\nUniform statistics:")
    print(f"  Mean:      {mean:.6f} (expected 0.5000)")
    print(f"  Variance:  {variance:.6f} (expected 0.0833)")
    print(f"  Min:       {min(samples):.6f}")
    print(f"  Max:       {max(samples):.6f}")

    # Generate a large batch of normal samples
    print("\nGenerating 50,000 normal samples...")
    start = time.time()
    samples = gen.normal(0, 1, n=50_000)
    elapsed = time.time() - start
    print(f"Generated {len(samples)} samples in {elapsed:.2f} seconds")
    print(f"Throughput: {len(samples) / elapsed:.0f} samples/second")

    # Compute basic statistics
    mean = sum(samples) / len(samples)
    variance = sum((s - mean) ** 2 for s in samples) / len(samples)
    print(f"\nNormal statistics:")
    print(f"  Mean:      {mean:.6f} (expected 0.0000)")
    print(f"  Variance:  {variance:.6f} (expected 1.0000)")
    print(f"  Min:       {min(samples):.6f}")
    print(f"  Max:       {max(samples):.6f}")

    # Generate a large batch of exponential samples
    print("\nGenerating 50,000 exponential samples...")
    start = time.time()
    samples = gen.exponential(1, n=50_000)
    elapsed = time.time() - start
    print(f"Generated {len(samples)} samples in {elapsed:.2f} seconds")

    mean = sum(samples) / len(samples)
    variance = sum((s - mean) ** 2 for s in samples) / len(samples)
    print(f"\nExponential statistics:")
    print(f"  Mean:      {mean:.6f} (expected 1.0000)")
    print(f"  Variance:  {variance:.6f} (expected 1.0000)")

    gen.stop()
    print("\nΦ")


if __name__ == '__main__':
    main()
