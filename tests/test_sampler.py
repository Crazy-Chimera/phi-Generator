"""
Tests for the SamplerLoop.
"""
import pytest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiSourceLoop, SamplerLoop
from phi_generator.types import SamplerConfig, DistributionType


class TestSamplerLoop:
    """Test the SamplerLoop class."""

    def setup_method(self):
        """Set up a sampler with a live source for each test."""
        self.source = PhiSourceLoop()
        self.source.start()
        self.sampler = SamplerLoop(self.source)

    def teardown_method(self):
        """Clean up after each test."""
        self.source.stop()

    def test_uniform_bounds(self):
        """Test that uniform samples respect bounds."""
        samples = self.sampler.sample_uniform(10, 5.0, 10.0)
        assert len(samples) == 10
        assert all(5.0 <= s <= 10.0 for s in samples)

    def test_uniform_distribution(self):
        """Test that uniform samples have the correct mean."""
        samples = self.sampler.sample_uniform(1000)
        assert len(samples) == 1000
        arr = np.array(samples)
        assert 0.45 < np.mean(arr) < 0.55

    def test_normal_distribution(self):
        """Test that normal samples have the correct mean and std."""
        samples = self.sampler.sample_normal(1000, mean=10, std=2)
        assert len(samples) == 1000
        arr = np.array(samples)
        assert 9.5 < np.mean(arr) < 10.5
        assert 1.5 < np.std(arr) < 2.5

    def test_exponential_distribution(self):
        """Test that exponential samples have the correct mean."""
        samples = self.sampler.sample_exponential(1000, rate=2.0)
        assert len(samples) == 1000
        arr = np.array(samples)
        assert all(s >= 0 for s in samples)
        assert 0.4 < np.mean(arr) < 0.6

    def test_sample_generic(self):
        """Test the generic sample method."""
        samples = self.sampler.sample("uniform", 5, min=0, max=1)
        assert len(samples) == 5

    def test_sample_generic_invalid(self):
        """Test that an unsupported distribution raises ValueError."""
        with pytest.raises(ValueError):
            self.sampler.sample("invalid_distribution", 5)

    def test_observe(self):
        """Test that observe returns the expected metrics."""
        metrics = self.sampler.observe({})
        assert 'output_queue_size' in metrics
        assert 'total_samples_generated' in metrics
        assert 'consumed_bits_per_sample' in metrics

    def test_evaluate(self):
        """Test that evaluate returns a non‑negative score."""
        metrics = self.sampler.observe({})
        score = self.sampler.evaluate(metrics)
        assert score >= 0

    def test_mutate(self):
        """Test that mutate adjusts parameters."""
        original_bits = self.sampler.config.bits_per_sample
        memory, policy = self.sampler.mutate({}, {}, 2.0)
        assert self.sampler.config.bits_per_sample <= original_bits

    def test_termination_condition(self):
        """Test that termination_condition is always False."""
        metrics = self.sampler.observe({})
        assert self.sampler.termination_condition(metrics) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
