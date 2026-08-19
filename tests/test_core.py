"""
Tests for the PhiGenerator core class.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiGenerator
from phi_generator.types import EleganceMetric


class TestPhiGenerator:
    """Test the main PhiGenerator class."""

    def test_singleton(self):
        """Test that a generator can be created."""
        gen = PhiGenerator()
        assert gen is not None

    def test_start_stop(self):
        """Test that start and stop work correctly."""
        gen = PhiGenerator()
        gen.start()
        assert gen._started is True
        gen.stop()
        assert gen._started is False

    def test_context_manager(self):
        """Test using the generator as a context manager."""
        with PhiGenerator() as gen:
            assert gen._started is True
        assert gen._started is False

    def test_random(self):
        """Test that random() returns a value in [0, 1]."""
        gen = PhiGenerator()
        gen.start()
        value = gen.random()
        assert isinstance(value, float)
        assert 0.0 <= value <= 1.0
        gen.stop()

    def test_uniform(self):
        """Test that uniform() returns values in the given range."""
        gen = PhiGenerator()
        gen.start()
        samples = gen.uniform(10, 20, n=10)
        assert len(samples) == 10
        assert all(10 <= s <= 20 for s in samples)
        gen.stop()

    def test_normal(self):
        """Test that normal() returns the correct number of samples."""
        gen = PhiGenerator()
        gen.start()
        samples = gen.normal(100, 15, n=10)
        assert len(samples) == 10
        gen.stop()

    def test_exponential(self):
        """Test that exponential() returns non‑negative samples."""
        gen = PhiGenerator()
        gen.start()
        samples = gen.exponential(0.5, n=10)
        assert len(samples) == 10
        assert all(s >= 0 for s in samples)
        gen.stop()

    def test_get_elegance(self):
        """Test that get_elegance() returns a valid EleganceMetric."""
        gen = PhiGenerator()
        gen.start()
        metrics = gen.get_elegance(sample_size=100)
        assert isinstance(metrics, EleganceMetric)
        assert metrics.samples_generated > 0
        gen.stop()

    def test_get_status(self):
        """Test that get_status() returns the expected structure."""
        gen = PhiGenerator()
        gen.start()
        status = gen.get_status()
        assert 'source' in status
        assert 'sampler' in status
        assert 'monitor' in status
        gen.stop()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
