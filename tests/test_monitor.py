"""
Tests for the EleganceMonitorLoop.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phi_generator import PhiSourceLoop, SamplerLoop, EleganceMonitorLoop
from phi_generator.types import EleganceMetric


class TestEleganceMonitorLoop:
    """Test the EleganceMonitorLoop class."""

    def setup_method(self):
        """Set up a monitor with live source and sampler."""
        self.source = PhiSourceLoop()
        self.source.start()
        self.sampler = SamplerLoop(self.source)
        self.monitor = EleganceMonitorLoop(self.source, self.sampler)

    def teardown_method(self):
        """Stop the source after each test."""
        self.source.stop()

    def test_evaluate(self):
        """Test that evaluate returns a valid EleganceMetric."""
        metric = self.monitor.evaluate(sample_size=200)
        assert isinstance(metric, EleganceMetric)
        assert metric.samples_generated > 0
        assert metric.score >= 0

    def test_evaluation_history(self):
        """Test that evaluation history is tracked."""
        self.monitor.evaluate(sample_size=100)
        self.monitor.evaluate(sample_size=100)
        assert len(self.monitor.history) == 2

    def test_observe(self):
        """Test that observe returns the expected metrics."""
        metrics = self.monitor.observe({})
        assert 'elegance_score' in metrics
        assert 'evaluation_count' in metrics

    def test_control(self):
        """Test that control returns a valid action."""
        metrics = self.monitor.observe({})
        result = self.monitor.control(metrics, {}, {})
        assert result['action'] in ('monitoring', 'mutated')

    def test_termination_condition(self):
        """Test that termination_condition is always False."""
        metrics = self.monitor.observe({})
        assert self.monitor.termination_condition(metrics) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
