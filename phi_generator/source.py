"""
PhiSourceLoop – Physical entropy source for the Φ‑Generator.
"""
import time
import math
import threading
from collections import deque
from typing import List, Dict, Any, Optional
import numpy as np

from .types import SourceConfig, SourceType, SourceReading
from .utils import generate_seed_from_time, calculate_entropy


class PhiSourceLoop:
    """
    Measures fluctuations of the Φ field and converts them to raw bits.

    In a real deployment, this would read from a physical sensor
    (qubit decoherence, EEG noise, network jitter).
    In simulation, it uses a chaotic map with drifting parameter
    to emulate the behavior of the Φ field.
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        self.name = "PhiSource"
        self.config = config or SourceConfig()
        self.raw_bitstream: deque = deque(maxlen=100_000)
        self.last_phi: float = 0.5
        self.source_quality: float = 0.5
        self.entropy_per_bit: float = 0.0
        self.total_bits_generated: int = 0
        self.consecutive_failures: int = 0
        self._running = False
        self._seed = self.config.seed or generate_seed_from_time()
        self._rng = np.random.default_rng(self._seed)
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start the Φ source and begin producing bits."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop the Φ source."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run(self):
        """Main production loop."""
        while self._running:
            reading = self._measure_phi()
            bits = self._reading_to_bits(reading)
            with self._lock:
                self.raw_bitstream.extend(bits)
                self.last_phi = reading.phi
                self.source_quality = reading.quality
                self.total_bits_generated += len(bits)
                window = list(self.raw_bitstream)[-1000:]
                self.entropy_per_bit = calculate_entropy(window) if window else 0.0
                if reading.quality < self.config.quality_threshold:
                    self.consecutive_failures += 1
                else:
                    self.consecutive_failures = 0
            time.sleep(self.config.throttle_ms / 1000.0)

    def _measure_phi(self) -> SourceReading:
        """
        Measure a Φ fluctuation.
        In simulation, uses a chaotic map.
        In production, this would interface with physical sensors.
        """
        self._seed = (
            self._seed * 6364136223846793005 + 1442695040888963407
        ) % (2 ** 64)
        raw = (self._seed >> 32) ^ (self._seed & 0xFFFFFFFF)
        phi = 0.5 + 0.5 * math.sin(self._seed / 1e10)
        phi = max(0.0, min(1.0, phi))
        quality = min(1.0, self.entropy_per_bit + 0.1)
        return SourceReading(
            raw_value=raw,
            phi=phi,
            timestamp=time.time(),
            quality=quality,
        )

    def _reading_to_bits(self, reading: SourceReading) -> List[int]:
        """Convert a Φ reading into a list of bits."""
        bits = []
        n = self.config.bits_per_cycle
        for i in range(n):
            bits.append((reading.raw_value >> i) & 1)
        return bits

    def get_bits(self, n: int, timeout: float = 5.0) -> List[int]:
        """
        Get n raw bits from the buffer, waiting if necessary.

        Args:
            n: Number of bits to retrieve.
            timeout: Maximum time to wait in seconds.

        Returns:
            List of n bits, or an empty list on timeout.
        """
        deadline = time.time() + timeout
        while len(self.raw_bitstream) < n:
            if time.time() > deadline:
                return []
            time.sleep(0.001)
        with self._lock:
            bits = [self.raw_bitstream.popleft() for _ in range(n)]
        return bits

    def get_status(self) -> Dict[str, Any]:
        """Return the current status of the source."""
        return {
            "running": self._running,
            "buffer_size": len(self.raw_bitstream),
            "last_phi": self.last_phi,
            "source_quality": self.source_quality,
            "entropy_per_bit": self.entropy_per_bit,
            "total_bits_generated": self.total_bits_generated,
            "consecutive_failures": self.consecutive_failures,
        }

    def observe(self, external_input: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS observe – derive metrics from state."""
        return {
            "buffer_size": len(self.raw_bitstream),
            "entropy_per_bit": self.entropy_per_bit,
            "source_quality": self.source_quality,
            "last_phi": self.last_phi,
        }

    def control(self, metrics: Dict[str, Any], memory: Dict[str, Any],
                policy: Dict[str, Any]) -> Dict[str, Any]:
        """LoopOS control – decide on action."""
        if metrics["buffer_size"] < 1000 and not self._running:
            self.start()
        if metrics["source_quality"] < self.config.quality_threshold:
            return {"action": "increase_throttle"}
        return {"action": "maintain"}

    def evaluate(self, metrics: Dict[str, Any]) -> float:
        """LoopOS evaluate – compute C/K elegance."""
        C = metrics["buffer_size"] * 0.001 + 0.01
        K = metrics["entropy_per_bit"]
        return C / max(K, 1e-6)

    def mutate(self, memory: Dict[str, Any], policy: Dict[str, Any],
               elegance: float) -> tuple:
        """LoopOS mutate – adjust source parameters for better elegance."""
        if elegance > 1.0 and self.config.throttle_ms > 0.1:
            self.config.throttle_ms *= 0.9
        elif elegance < 0.5 and self.config.throttle_ms < 10.0:
            self.config.throttle_ms *= 1.1
        return memory, policy

    def termination_condition(self, metrics: Dict[str, Any]) -> bool:
        """LoopOS termination – source runs forever."""
        return False
