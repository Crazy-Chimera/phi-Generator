"""
Tests for utility functions.
"""
import pytest
import sys
import os
import math
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator.utils import (
    calculate_entropy,
    calculate_autocorrelation,
    calculate_chi_square,
    validate_bounds,
    generate_seed_from_time,
    map_to_range,
)


class TestUtils:
    """Test utility functions."""

    def test_entropy_empty(self):
        """Test entropy on empty list."""
        assert calculate_entropy([]) == 0.0

    def test_entropy_zero_variation(self):
        """Test entropy on all zeros."""
        assert calculate_entropy([0] * 100) == 0.0

    def test_entropy_full(self):
        """Test entropy on uniform bits."""
        bits = [0] * 50 + [1] * 50
        entropy = calculate_entropy(bits)
        assert entropy > 0.99

    def test_autocorrelation_empty(self):
        """Test autocorrelation on empty list."""
        assert calculate_autocorrelation([]) == 0.0

    def test_autocorrelation_random(self):
        """Test autocorrelation on random data."""
        data = list(np.random.rand(1000))
        autocorr = calculate_autocorrelation(data)
        assert abs(autocorr) < 0.1

    def test_autocorrelation_constant(self):
        """Test autocorrelation on constant data."""
        data = [1.0] * 100
        autocorr = calculate_autocorrelation(data)
        assert autocorr == 0.0

    def test_chi_square_empty(self):
        """Test chi‑square on empty list."""
        assert calculate_chi_square([]) == float('inf')

    def test_chi_square_uniform(self):
        """Test chi‑square on uniform data."""
        data = list(np.random.rand(10000))
        chi = calculate_chi_square(data)
        assert chi < 0.1

    def test_validate_bounds_sorted(self):
        """Test validate_bounds with already sorted bounds."""
        low, high = validate_bounds(1, 2)
        assert low == 1
        assert high == 2

    def test_validate_bounds_reversed(self):
        """Test validate_bounds with reversed bounds."""
        low, high = validate_bounds(2, 1)
        assert low == 1
        assert high == 2

    def test_generate_seed(self):
        """Test that seed generation returns a positive integer."""
        seed = generate_seed_from_time()
        assert isinstance(seed, int)
        assert seed > 0

    def test_map_to_range(self):
        """Test map_to_range."""
        assert map_to_range(0.0, 10, 20) == 10.0
        assert map_to_range(1.0, 10, 20) == 20.0
        assert map_to_range(0.5, 10, 20) == 15.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
