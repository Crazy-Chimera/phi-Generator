"""
EleganceMonitorLoop – Quality control for the Φ‑Generator.
"""
import time
from typing import List, Dict, Any, Optional

from .source import PhiSourceLoop
from .sampler import SamplerLoop
from .types import EleganceMetric
from .tests import StatisticalTestSuite


class EleganceMonitorLoop:
    """
    Monitors the elegance C/K of the generator and triggers mutations
    when quality degrades.
    """

    def __init__(self, source: PhiSourceLoop, sampler: SamplerLoop,
                 test_suite: Optional[StatisticalTestSuite] = None):
        self.name = "EleganceMonitor"
        self.source = source
        self.sampler = sampler
        self.test_suite = test_suite or StatisticalTestSuite()
        self.elegance_score: float = float('inf')
        self.history: List[float] = []
        self.test_results: Dict[str, Any] = {}
        self.last_evaluation_time: float = 0.0
        self.evaluation_count: int = 0

    def evaluate(self, sample_size: int = 1000) -> EleganceMetric:
        """
        Run statistical tests on generated samples and compute C/K.

        Args:
            sample_size: Number of samples to generate for testing.

        Returns:
            EleganceMetric with the current C/K ratio.
        """
        metric = EleganceMetric()
        metric.timestamp = time.time()
        samples = self.sampler.sample_uniform(sample_size, 0.0, 1.0)
        metric.samples_generated = len(samples)
        metric.bits_consumed = int(len(samples) * self.sampler.consumed_bits_per_sample)
        if not samples:
            return metric
        self.test_suite.run(samples)
        metric.chi_square = self.test_suite.chi_square
        metric.autocorrelation = self.test_suite.autocorrelation
        metric.entropy_per_bit = self.source.entropy_per_bit
        metric.complexity = metric.bits_consumed * 0.001 + 0.01
        penalty = min(1.0, abs(metric.chi_square) + abs(metric.autocorrelation) * 10)
        metric.consistency = 1.0 - penalty
        metric.score = metric.complexity / max(metric.consistency, 1e-6)
        metric.confidence = 0.85
        metric.explanation = (
            f"C={metric.complexity:.4f}, K={metric.consistency:.4f}, "
            f"chi_sq={metric.chi_square:.6f}, autocorr={metric.autocorrelation:.6f}"
        )
        self.elegance_score = metric.score
        self.history.append(metric.score)
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        self.test_results = metric.to_dict()
        self.last_evaluation_time = time.time()
        self.evaluation_count += 1
        return metric

    def observe(self, external_input: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS observe – derive metrics from state."""
        return {
            "elegance_score": self.elegance_score,
            "history_length": len(self.history),
            "evaluation_count": self.evaluation_count,
        }

    def control(self, metrics: Dict[str, Any], memory: Dict[str, Any],
                policy: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS control – decide on action."""
        if metrics["elegance_score"] > 1.0:
            self.sampler.mutate({}, {}, metrics["elegance_score"])
            self.source.mutate({}, {}, metrics["elegance_score"])
            return {"action": "mutated"}
        return {"action": "monitoring"}

    def evaluate_own(self, metrics: Dict[str, Any]) -> float:
        """LoopOS evaluate – compute own elegance."""
        C = metrics["evaluation_count"] * 0.01
        K = max(0.1, 1.0 / max(metrics["elegance_score"], 1e-6))
        return C / max(K, 1e-6)

    def termination_condition(self, metrics: Dict[str, Any]) -> bool:
        """LoopOS termination – monitor runs forever."""
        return False
