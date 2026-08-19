"""
Type definitions for the Φ‑Generator.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import time


class SourceType(Enum):
    """Type of physical entropy source for the Φ field."""
    SIMULATED_PHI = "simulated_phi"
    QUBIT_DECOHERENCE = "qubit_decoherence"
    NETWORK_JITTER = "network_jitter"
    EEG_NOISE = "eeg_noise"
    CLOCK_DRIFT = "clock_drift"


class DistributionType(Enum):
    """Supported target distributions."""
    UNIFORM = "uniform"
    NORMAL = "normal"
    EXPONENTIAL = "exponential"
    POISSON = "poisson"
    CAUCHY = "cauchy"


@dataclass
class SourceConfig:
    """Configuration for a Φ source."""
    source_type: SourceType = SourceType.SIMULATED_PHI
    bits_per_cycle: int = 8
    throttle_ms: float = 1.0
    quality_threshold: float = 0.9
    max_consecutive_failures: int = 100
    seed: Optional[int] = None


@dataclass
class SamplerConfig:
    """Configuration for a sampler."""
    distribution: DistributionType = DistributionType.UNIFORM
    parameters: Dict[str, float] = field(default_factory=lambda: {"min": 0.0, "max": 1.0})
    bits_per_sample: int = 32
    bits_per_normal_pair: int = 64
    max_retries: int = 100


@dataclass
class EleganceMetric:
    """Structured result of elegance evaluation."""
    score: float = float('inf')
    complexity: float = 0.0
    consistency: float = 0.0
    entropy_per_bit: float = 0.0
    chi_square: float = 0.0
    autocorrelation: float = 0.0
    bits_consumed: int = 0
    samples_generated: int = 0
    constraints_satisfied: List[str] = field(default_factory=list)
    constraints_violated: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    regressions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the metric to a dictionary."""
        return {
            "score": self.score,
            "complexity": self.complexity,
            "consistency": self.consistency,
            "entropy_per_bit": self.entropy_per_bit,
            "chi_square": self.chi_square,
            "autocorrelation": self.autocorrelation,
            "bits_consumed": self.bits_consumed,
            "samples_generated": self.samples_generated,
            "constraints_satisfied": self.constraints_satisfied,
            "constraints_violated": self.constraints_violated,
            "improvements": self.improvements,
            "regressions": self.regressions,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "timestamp": self.timestamp,
        }


@dataclass
class SourceReading:
    """One reading from the Φ source."""
    raw_value: int
    phi: float
    timestamp: float
    quality: float


@dataclass
class SampleBatch:
    """A batch of generated samples."""
    samples: List[float]
    distribution: DistributionType
    parameters: Dict[str, float]
    bits_consumed: int
    generated_at: float
    source_quality: float
