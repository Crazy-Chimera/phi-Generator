"""
Tests for the PhiSourceLoop.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiSourceLoop
from phi_generator.types import SourceConfig, SourceType


class TestPhiSourceLoop:
    """Test the PhiSourceLoop class."""

    def setup_method(self):
        """Set up a running source for each test."""
        self.source = PhiSourceLoop()
        self.source.start()

    def teardown_method(self):
        """Stop the source after each test."""
        self.source.stop()

    def test_start_stop(self):
        """Test that start and stop work."""
        assert self.source._running is True
        self.source.stop()
        assert self.source._running is False

    def test_get_bits(self):
        """Test that get_bits returns the correct number of bits."""
        bits = self.source.get_bits(100, timeout=3.0)
        assert len(bits) == 100
        assert all(b in (0, 1) for b in bits)

    def test_bits_varied(self):
        """Test that bits contain both 0 and 1."""
        bits = self.source.get_bits(1000, timeout=5.0)
        ones = sum(bits)
        zeros = len(bits) - ones
        assert ones > 0
        assert zeros > 0

    def test_get_status(self):
        """Test that get_status returns the expected fields."""
        status = self.source.get_status()
        assert status['running'] is True
        assert status['buffer_size'] >= 0
        assert 0.0 <= status['last_phi'] <= 1.0
        assert 'entropy_per_bit' in status

    def test_observe(self):
        """Test that observe returns the expected metrics."""
        metrics = self.source.observe({})
        assert 'entropy_per_bit' in metrics
        assert 'source_quality' in metrics
        assert 'last_phi' in metrics

    def test_evaluate(self):
        """Test that evaluate returns a non‑negative score."""
        metrics = self.source.observe({})
        score = self.source.evaluate(metrics)
        assert score >= 0

    def test_mutate(self):
        """Test that mutate adjusts throttle rate."""
        original_throttle = self.source.config.throttle_ms
        memory, policy = self.source.mutate({}, {}, 2.0)
        assert self.source.config.throttle_ms <= original_throttle

    def test_termination_condition(self):
        """Test that termination_condition is always False."""
        metrics = self.source.observe({})
        assert self.source.termination_condition(metrics) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
