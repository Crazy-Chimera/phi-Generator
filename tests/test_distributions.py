"""
Tests for distribution functions.
"""
import pytest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator.distributions import (
    uniform_from_bits,
    normal_from_bits,
    exponential_from_bits,
)
from phi_generator.utils import bits_to_int, int_to_bits


class TestDistributions:
    """Test distribution transformation functions."""

    def test_uniform_from_bits_zero(self):
        """Test uniform_from_bits with all zero bits."""
        bits = [0] * 32
        sample = uniform_from_bits(bits, 0, 1)
        assert sample == 0.0

    def test_uniform_from_bits_all_ones(self):
        """Test uniform_from_bits with all one bits."""
        bits = [1] * 32
        sample = uniform_from_bits(bits, 0, 1)
        assert sample > 0.99
        assert sample < 1.0

    def test_uniform_from_bits_range(self):
        """Test uniform_from_bits with a custom range."""
        bits = [0] * 32
        sample = uniform_from_bits(bits, 5, 10)
        assert sample == 5.0

    def test_uniform_from_bits_empty(self):
        """Test uniform_from_bits with empty bits."""
        sample = uniform_from_bits([], 0, 1)
        assert sample == 0.0

    def test_normal_from_bits(self):
        """Test that normal_from_bits returns a float."""
        bits = [1, 0, 1, 0] * 16
        sample = normal_from_bits(bits)
        assert isinstance(sample, float)

    def test_exponential_from_bits(self):
        """Test that exponential_from_bits returns non‑negative."""
        bits = [0, 1] * 16
        sample = exponential_from_bits(bits)
        assert sample >= 0

    def test_bits_to_int(self):
        """Test bits_to_int conversion."""
        assert bits_to_int([0, 0, 0, 1]) == 1
        assert bits_to_int([1, 0, 0, 0]) == 8
        assert bits_to_int([1, 1, 1, 1]) == 15

    def test_int_to_bits(self):
        """Test int_to_bits conversion."""
        assert int_to_bits(1, 4) == [0, 0, 0, 1]
        assert int_to_bits(8, 4) == [1, 0, 0, 0]
        assert int_to_bits(15, 4) == [1, 1, 1, 1]

    def test_bits_roundtrip(self):
        """Test that bits_to_int and int_to_bits are inverses."""
        for value in [0, 1, 42, 255]:
            bits = int_to_bits(value, 8)
            assert bits_to_int(bits) == value


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
