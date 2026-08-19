"""
Helper functions for the Φ‑Generator.
"""
import math
import hashlib
import time
from typing import List, Tuple, Dict, Any
import numpy as np


def bits_to_int(bits: List[int]) -> int:
    """
    Convert a list of bits (MSB first) to an integer.

    Args:
        bits: List of 0/1 integers.

    Returns:
        Integer value of the bit sequence.
    """
    value = 0
    for bit in bits:
        value = (value << 1) | (bit & 1)
    return value


def int_to_bits(value: int, num_bits: int) -> List[int]:
    """
    Convert an integer to a list of bits (MSB first).

    Args:
        value: Integer to convert.
        num_bits: Number of bits to produce.

    Returns:
        List of 0/1 integers.
    """
    bits = []
    for i in range(num_bits - 1, -1, -1):
        bits.append((value >> i) & 1)
    return bits


def calculate_entropy(data: List[int]) -> float:
    """
    Calculate Shannon entropy (in bits) of a binary sequence.

    Args:
        data: List of 0/1 integers.

    Returns:
        Entropy per bit in the range [0, 1].
    """
    if not data:
        return 0.0
    ones = sum(data)
    zeros = len(data) - ones
    p1 = ones / len(data)
    p0 = zeros / len(data)
    entropy = 0.0
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    return entropy


def calculate_autocorrelation(data: List[float], lag: int = 1) -> float:
    """
    Calculate the lag‑k autocorrelation of a sequence.

    Args:
        data: List of floats.
        lag: Lag for autocorrelation.

    Returns:
        Autocorrelation in [-1, 1].
    """
    if len(data) < lag + 2:
        return 0.0
    arr = np.array(data, dtype=np.float64)
    n = len(arr)
    mean = np.mean(arr)
    var = np.var(arr)
    if var == 0:
        return 0.0
    corr = np.sum((arr[:-lag] - mean) * (arr[lag:] - mean)) / ((n - lag) * var)
    return float(corr)


def calculate_chi_square(
    samples: List[float],
    bins: int = 10,
    range_min: float = 0.0,
    range_max: float = 1.0,
) -> float:
    """
    Calculate chi‑square statistic for uniformity test.

    Args:
        samples: List of floats.
        bins: Number of histogram bins.
        range_min: Minimum value for the histogram.
        range_max: Maximum value for the histogram.

    Returns:
        Chi‑square statistic normalized by sample count. Lower is better.
    """
    if not samples:
        return float('inf')
    hist, _ = np.histogram(samples, bins=bins, range=(range_min, range_max))
    expected = len(samples) / bins
    if expected == 0:
        return float('inf')
    chi_sq = np.sum((hist - expected) ** 2 / expected) / len(samples)
    return float(chi_sq)


def validate_bounds(low: float, high: float) -> Tuple[float, float]:
    """
    Validate that low < high.

    Args:
        low: Lower bound.
        high: Upper bound.

    Returns:
        Sorted bounds as (min, max).
    """
    if low > high:
        return high, low
    return low, high


def generate_seed_from_time() -> int:
    """
    Generate a seed from the current time and entropy.

    Returns:
        64‑bit integer seed.
    """
    time_bytes = str(time.time_ns()).encode()
    return int.from_bytes(hashlib.sha256(time_bytes).digest()[:8], 'big')


def map_to_range(value: float, low: float, high: float) -> float:
    """
    Map a value from [0, 1] to [low, high].

    Args:
        value: Input value in [0, 1].
        low: Target lower bound.
        high: Target upper bound.

    Returns:
        Mapped value in [low, high].
    """
    return low + value * (high - low)
