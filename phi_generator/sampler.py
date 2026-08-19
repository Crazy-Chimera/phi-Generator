"""
SamplerLoop – Transform raw bits into samples from target distributions.
"""
import time
from collections import deque
from typing import List, Dict, Any, Optional

from .source import PhiSourceLoop
from .types import SamplerConfig, DistributionType
from .distributions import uniform_from_bits, normal_from_bits, exponential_from_bits
from .utils import validate_bounds


class SamplerLoop:
    """
    Converts raw bits from PhiSourceLoop into samples from a target
    distribution, following the LoopOS pattern.
    """

    def __init__(self, source: PhiSourceLoop, config: Optional[SamplerConfig] = None):
        self.name = "Sampler"
        self.source = source
        self.config = config or SamplerConfig()
        self.output_queue: deque = deque(maxlen=10_000)
        self.consumed_bits_per_sample: float = 0.0
        self.total_samples_generated: int = 0
        self.last_generation_time: float = 0.0

    def sample_uniform(self, n: int = 1, min_val: Optional[float] = None,
                       max_val: Optional[float] = None) -> List[float]:
        """
        Generate n samples from the uniform distribution.

        Args:
            n: Number of samples.
            min_val: Lower bound.
            max_val: Upper bound.

        Returns:
            List of n uniform samples.
        """
        if min_val is None:
            min_val = self.config.parameters.get("min", 0.0)
        if max_val is None:
            max_val = self.config.parameters.get("max", 1.0)
        min_val, max_val = validate_bounds(min_val, max_val)
        bit_count = self.config.bits_per_sample
        samples = []
        for _ in range(n):
            bits = self.source.get_bits(bit_count)
            if len(bits) < bit_count:
                return samples
            sample = uniform_from_bits(bits, min_val, max_val)
            samples.append(sample)
            self.output_queue.append(sample)
        self.consumed_bits_per_sample = bit_count
        self.total_samples_generated += len(samples)
        self.last_generation_time = time.time()
        return samples

    def sample_normal(self, n: int = 1, mean: Optional[float] = None,
                      std: Optional[float] = None) -> List[float]:
        """
        Generate n samples from the normal distribution using Box‑Muller.

        Args:
            n: Number of samples.
            mean: Mean of the distribution.
            std: Standard deviation.

        Returns:
            List of n normal samples.
        """
        if mean is None:
            mean = self.config.parameters.get("mean", 0.0)
        if std is None:
            std = self.config.parameters.get("std", 1.0)
        bit_count = self.config.bits_per_normal_pair // 2
        samples = []
        for _ in range((n + 1) // 2):
            bits = self.source.get_bits(bit_count * 2)
            if len(bits) < bit_count * 2:
                return samples
            z1 = normal_from_bits(bits, mean, std)
            z2 = normal_from_bits(bits[::-1], mean, std)
            samples.append(z1)
            samples.append(z2)
        result = samples[:n]
        self.consumed_bits_per_sample = bit_count * 2 / max(len(result), 1)
        self.total_samples_generated += len(result)
        self.last_generation_time = time.time()
        return result

    def sample_exponential(self, n: int = 1, rate: Optional[float] = None) -> List[float]:
        """
        Generate n samples from the exponential distribution.

        Args:
            n: Number of samples.
            rate: Rate parameter.

        Returns:
            List of n exponential samples.
        """
        if rate is None:
            rate = self.config.parameters.get("rate", 1.0)
        bit_count = self.config.bits_per_sample
        samples = []
        for _ in range(n):
            bits = self.source.get_bits(bit_count)
            if len(bits) < bit_count:
                return samples
            sample = exponential_from_bits(bits, rate)
            samples.append(sample)
        self.consumed_bits_per_sample = bit_count
        self.total_samples_generated += len(samples)
        self.last_generation_time = time.time()
        return samples

    def sample(self, distribution: str, n: int = 1, **params) -> List[float]:
        """
        Generate n samples from the specified distribution.

        Args:
            distribution: Name of the distribution.
            n: Number of samples.
            **params: Distribution parameters.

        Returns:
            List of n samples.
        """
        dist = DistributionType(distribution)
        if dist == DistributionType.UNIFORM:
            return self.sample_uniform(n, params.get("min"), params.get("max"))
        elif dist == DistributionType.NORMAL:
            return self.sample_normal(n, params.get("mean"), params.get("std"))
        elif dist == DistributionType.EXPONENTIAL:
            return self.sample_exponential(n, params.get("rate"))
        else:
            raise ValueError(f"Unsupported distribution: {dist}")

    def observe(self, external_input: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS observe – derive metrics from state."""
        return {
            "output_queue_size": len(self.output_queue),
            "total_samples_generated": self.total_samples_generated,
            "consumed_bits_per_sample": self.consumed_bits_per_sample,
        }

    def control(self, metrics: Dict[str, Any], memory: Dict[str, Any],
                policy: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS control – decide on action."""
        if metrics["output_queue_size"] < 100:
            self.sample_uniform(50)
            return {"action": "generated"}
        return {"action": "idle"}

    def evaluate(self, metrics: Dict[str, Any]) -> float:
        """LoopOS evaluate – compute C/K elegance."""
        C = metrics["consumed_bits_per_sample"] * 0.01
        K = 0.9
        return C / max(K, 1e-6)

    def mutate(self, memory: Dict[str, Any], policy: Dict[str, Any],
               elegance: float) -> tuple:
        """LoopOS mutate – adjust sampling parameters."""
        if elegance > 1.0 and self.config.bits_per_sample > 16:
            self.config.bits_per_sample -= 4
        elif elegance < 0.3 and self.config.bits_per_sample < 64:
            self.config.bits_per_sample += 4
        return memory, policy

    def termination_condition(self, metrics: Dict[str, Any]) -> bool:
        """LoopOS termination – sampler runs forever."""
        return False
