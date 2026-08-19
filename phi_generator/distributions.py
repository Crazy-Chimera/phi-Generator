"""
Distribution functions for the Φ‑Generator.
All functions transform raw bits into samples from target distributions.
"""
import math
from typing import List
from .utils import bits_to_int


def uniform_from_bits(bits: List[int], min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Transform a list of bits into a uniform sample in [min_val, max_val].

    Args:
        bits: List of 0/1 integers.
        min_val: Lower bound.
        max_val: Upper bound.

    Returns:
        Uniform sample in [min_val, max_val].
    """
    num_bits = len(bits)
    if num_bits == 0:
        return min_val
    raw = bits_to_int(bits)
    u = raw / (2 ** num_bits)
    return min_val + u * (max_val - min_val)


def normal_from_bits(bits: List[int], mean: float = 0.0, std: float = 1.0) -> float:
    """
    Transform a list of bits into a normal sample using Box‑Muller transform.

    Args:
        bits: List of 0/1 integers.
        mean: Mean of the normal distribution.
        std: Standard deviation of the normal distribution.

    Returns:
        Normal sample.
    """
    num_bits = len(bits)
    if num_bits < 2:
        return mean
    half = num_bits // 2
    u1 = uniform_from_bits(bits[:half])
    u2 = uniform_from_bits(bits[half:2 * half])
    u1 = max(u1, 1e-12)
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    z = r * math.cos(theta)
    return mean + std * z


def exponential_from_bits(bits: List[int], rate: float = 1.0) -> float:
    """
    Transform a list of bits into an exponential sample using inverse CDF.

    Args:
        bits: List of 0/1 integers.
        rate: Rate parameter of the exponential distribution.

    Returns:
        Exponential sample.
    """
    num_bits = len(bits)
    if num_bits == 0:
        return 0.0
    raw = bits_to_int(bits)
    u = raw / (2 ** num_bits)
    u = max(u, 1e-12)
    return -math.log(u) / rate
