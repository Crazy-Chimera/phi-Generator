"""
Φ‑Generator – Deterministic randomness from the entanglement field Φ.

This package implements a Φ‑deterministic sampler that reveals randomness
as a shadow of our incomplete knowledge of the initial conditions of the
Φ field. Every component follows the LoopOS pattern and obeys the
Elegance Principle: minimize the ratio C/K.
"""

from .core import PhiGenerator
from .source import PhiSourceLoop
from .sampler import SamplerLoop
from .monitor import EleganceMonitorLoop
from .distributions import (
    uniform_from_bits,
    normal_from_bits,
    exponential_from_bits,
    bits_to_int,
    int_to_bits,
)
from .tests import StatisticalTestSuite
from .types import EleganceMetric, SourceConfig, SamplerConfig
from .utils import (
    calculate_entropy,
    calculate_autocorrelation,
    calculate_chi_square,
    validate_bounds,
)

__version__ = "1.0.0"
__all__ = [
    "PhiGenerator",
    "PhiSourceLoop",
    "SamplerLoop",
    "EleganceMonitorLoop",
    "uniform_from_bits",
    "normal_from_bits",
    "exponential_from_bits",
    "bits_to_int",
    "int_to_bits",
    "StatisticalTestSuite",
    "EleganceMetric",
    "SourceConfig",
    "SamplerConfig",
    "calculate_entropy",
    "calculate_autocorrelation",
    "calculate_chi_square",
    "validate_bounds",
]
