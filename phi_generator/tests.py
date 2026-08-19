"""
Statistical test suite for the Φ‑Generator.
"""
import math
from typing import List, Dict, Any
import numpy as np


class StatisticalTestSuite:
    """
    Battery of statistical tests to evaluate the quality of generated samples.
    """

    def __init__(self, bins: int = 10, significance_level: float = 0.05):
        self.bins = bins
        self.significance_level = significance_level
        self.chi_square: float = 0.0
        self.autocorrelation: float = 0.0
        self.entropy: float = 0.0
        self.kolmogorov_smirnov: float = 0.0
        self.all_passed: bool = False
        self.results: Dict[str, Any] = {}

    def run(self, samples: List[float]) -> Dict[str, Any]:
        """
        Run all tests on a list of samples.

        Args:
            samples: List of floats in [0, 1].

        Returns:
            Dictionary with test results.
        """
        arr = np.array(samples, dtype=np.float64)
        self.chi_square = self._chi_square_test(arr)
        self.autocorrelation = self._autocorrelation_test(arr)
        self.entropy = self._entropy_test(arr)
        self.kolmogorov_smirnov = self._ks_test(arr)
        self.all_passed = self._check_all()
        self.results = {
            "chi_square": self.chi_square,
            "autocorrelation": self.autocorrelation,
            "entropy": self.entropy,
            "kolmogorov_smirnov": self.kolmogorov_smirnov,
            "all_passed": self.all_passed,
        }
        return self.results

    def _chi_square_test(self, arr: np.ndarray) -> float:
        """Chi‑square test for uniformity."""
        if len(arr) == 0:
            return float('inf')
        hist, _ = np.histogram(arr, bins=self.bins, range=(0, 1))
        expected = len(arr) / self.bins
        if expected == 0:
            return float('inf')
        chi_sq = np.sum((hist - expected) ** 2 / expected) / len(arr)
        return float(chi_sq)

    def _autocorrelation_test(self, arr: np.ndarray, lag: int = 1) -> float:
        """Autocorrelation test."""
        if len(arr) < lag + 2:
            return 0.0
        n = len(arr)
        mean = np.mean(arr)
        var = np.var(arr)
        if var == 0:
            return 0.0
        corr = np.sum((arr[:-lag] - mean) * (arr[lag:] - mean)) / ((n - lag) * var)
        return float(corr)

    def _entropy_test(self, arr: np.ndarray) -> float:
        """Entropy test (normalized)."""
        if len(arr) == 0:
            return 0.0
        hist, _ = np.histogram(arr, bins=self.bins, range=(0, 1))
        probs = hist / len(arr)
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        max_entropy = math.log2(self.bins)
        return entropy / max_entropy if max_entropy > 0 else 0.0

    def _ks_test(self, arr: np.ndarray) -> float:
        """Kolmogorov‑Smirnov test statistic for uniformity."""
        if len(arr) == 0:
            return float('inf')
        sorted_arr = np.sort(arr)
        n = len(arr)
        d_plus = np.max(np.arange(1, n + 1) / n - sorted_arr)
        d_minus = np.max(sorted_arr - np.arange(0, n) / n)
        return float(max(d_plus, d_minus))

    def _check_all(self) -> bool:
        """Check if all tests pass."""
        chi_ok = self.chi_square < 0.1
        autocorr_ok = abs(self.autocorrelation) < 0.05
        entropy_ok = self.entropy > 0.9
        ks_ok = self.kolmogorov_smirnov < 0.1
        return chi_ok and autocorr_ok and entropy_ok and ks_ok
