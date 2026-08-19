"""
PhiGenerator – Main class for the Φ‑Generator.
"""
from typing import List, Dict, Any, Optional

from .source import PhiSourceLoop
from .sampler import SamplerLoop
from .monitor import EleganceMonitorLoop
from .types import SourceConfig, SamplerConfig, EleganceMetric


class PhiGenerator:
    """
    The Φ‑Generator. A deterministic randomness generator that operates
    according to the Theory of Everything's elegance principle.

    Example:
        gen = PhiGenerator()
        gen.start()
        value = gen.random()
        metrics = gen.get_elegance()
    """

    def __init__(
        self,
        source_config: Optional[SourceConfig] = None,
        sampler_config: Optional[SamplerConfig] = None,
    ):
        self.source = PhiSourceLoop(source_config)
        self.sampler = SamplerLoop(self.source, sampler_config)
        self.monitor = EleganceMonitorLoop(self.source, self.sampler)
        self._started = False

    def start(self):
        """Start the Φ source and begin generating."""
        if not self._started:
            self.source.start()
            self._started = True

    def stop(self):
        """Stop the Φ source."""
        if self._started:
            self.source.stop()
            self._started = False

    def random(self) -> float:
        """
        Return a uniform random sample in [0, 1].

        Returns:
            A float in [0, 1].
        """
        self.start()
        samples = self.sampler.sample_uniform(1)
        return samples[0] if samples else 0.0

    def uniform(self, low: float, high: float, n: int = 1) -> List[float]:
        """
        Return n uniform samples in [low, high].

        Args:
            low: Lower bound.
            high: Upper bound.
            n: Number of samples.

        Returns:
            List of n uniform samples.
        """
        self.start()
        return self.sampler.sample_uniform(n, low, high)

    def normal(self, mean: float = 0.0, std: float = 1.0, n: int = 1) -> List[float]:
        """
        Return n normal samples.

        Args:
            mean: Mean of the distribution.
            std: Standard deviation.
            n: Number of samples.

        Returns:
            List of n normal samples.
        """
        self.start()
        return self.sampler.sample_normal(n, mean, std)

    def exponential(self, rate: float = 1.0, n: int = 1) -> List[float]:
        """
        Return n exponential samples.

        Args:
            rate: Rate parameter.
            n: Number of samples.

        Returns:
            List of n exponential samples.
        """
        self.start()
        return self.sampler.sample_exponential(n, rate)

    def get_elegance(self, sample_size: int = 1000) -> EleganceMetric:
        """
        Return the current elegance metrics of the generator.

        Args:
            sample_size: Number of samples to generate for testing.

        Returns:
            EleganceMetric with the current C/K ratio.
        """
        self.start()
        return self.monitor.evaluate(sample_size)

    def get_status(self) -> Dict[str, Any]:
        """
        Return the current status of the entire generator.

        Returns:
            Dictionary with source, sampler, and monitor status.
        """
        return {
            "source": self.source.get_status(),
            "sampler": self.sampler.observe({}),
            "monitor": self.monitor.observe({}),
        }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
