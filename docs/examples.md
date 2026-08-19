# Φ‑Generator Examples

## Basic Usage

Generate random samples from different distributions.

```python
from phi_generator import PhiGenerator

# Create and start the generator
gen = PhiGenerator()
gen.start()

# Single uniform sample
value = gen.random()
print(f"Uniform [0,1]: {value:.6f}")

# Multiple uniform samples
samples = gen.uniform(10, 20, n=5)
print(f"Uniform [10,20]: {samples}")

# Normal samples
samples = gen.normal(100, 15, n=5)
print(f"Normal (100,15): {samples}")

# Exponential samples
samples = gen.exponential(0.5, n=5)
print(f"Exponential (0.5): {samples}")

gen.stop()
```

## Elegance Monitoring

Track the elegance of the generator over time.

```python
from phi_generator import PhiGenerator
import time

gen = PhiGenerator()
gen.start()

for cycle in range(10):
    metrics = gen.get_elegance(sample_size=500)
    print(f"Cycle {cycle}: Score={metrics.score:.4f}, "
          f"C={metrics.complexity:.4f}, K={metrics.consistency:.4f}")
    time.sleep(1)

gen.stop()
```

## Context Manager

Use the generator as a context manager.

```python
from phi_generator import PhiGenerator

with PhiGenerator() as gen:
    value = gen.random()
    print(f"Value: {value}")
```

## Batch Generation

Generate large batches efficiently.

```python
from phi_generator import PhiGenerator
import time

gen = PhiGenerator()
gen.start()

start = time.time()
samples = gen.uniform(0, 1, n=100_000)
elapsed = time.time() - start
print(f"Generated {len(samples)} samples in {elapsed:.2f} seconds")
print(f"Throughput: {len(samples) / elapsed:.0f} samples/second")

gen.stop()
```

## Advanced Configuration

Customize source and sampler parameters.

```python
from phi_generator import PhiGenerator, SourceConfig, SamplerConfig, SourceType

source_cfg = SourceConfig(
    source_type=SourceType.SIMULATED_PHI,
    bits_per_cycle=16,
    throttle_ms=0.5,
)

sampler_cfg = SamplerConfig(
    bits_per_sample=64,
    parameters={"min": 0.0, "max": 100.0},
)

gen = PhiGenerator(source_config=source_cfg, sampler_config=sampler_cfg)
gen.start()
samples = gen.uniform(0, 100, n=10)
print(f"Samples: {samples}")
gen.stop()
```
