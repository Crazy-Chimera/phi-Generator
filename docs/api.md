# Φ‑Generator API Reference

## PhiGenerator

The main class for the Φ‑Generator.

### Constructor

```python
PhiGenerator(source_config=None, sampler_config=None)
```

### Methods

#### `start()`

Start the Φ source and begin generating.

```python
gen = PhiGenerator()
gen.start()
```

#### `stop()`

Stop the Φ source.

```python
gen.stop()
```

#### `random() → float`

Return a uniform random sample in [0, 1].

```python
value = gen.random()
# value: 0.723456
```

#### `uniform(low, high, n=1) → List[float]`

Return n uniform samples in [low, high].

```python
samples = gen.uniform(10, 20, n=5)
# samples: [14.23, 11.87, 18.45, 10.02, 16.78]
```

#### `normal(mean=0.0, std=1.0, n=1) → List[float]`

Return n normal samples.

```python
samples = gen.normal(100, 15, n=5)
# samples: [98.45, 112.30, 95.12, 105.67, 99.90]
```

#### `exponential(rate=1.0, n=1) → List[float]`

Return n exponential samples.

```python
samples = gen.exponential(0.5, n=5)
# samples: [0.45, 1.23, 2.10, 0.89, 3.45]
```

#### `get_elegance(sample_size=1000) → EleganceMetric`

Run statistical tests and compute the C/K ratio.

```python
metrics = gen.get_elegance()
print(f"Elegance: {metrics.score:.4f}")
print(f"Complexity: {metrics.complexity:.4f}")
print(f"Consistency: {metrics.consistency:.4f}")
print(f"Entropy/bit: {metrics.entropy_per_bit:.4f}")
print(f"Chi‑square: {metrics.chi_square:.6f}")
print(f"Autocorrelation: {metrics.autocorrelation:.6f}")
```

#### `get_status() → Dict`

Return the current status of the entire generator.

```python
status = gen.get_status()
# status: {
#     "source": {...},
#     "sampler": {...},
#     "monitor": {...},
# }
```

## PhiSourceLoop

The physical entropy source.

### Constructor

```python
PhiSourceLoop(config=None)
```

### Methods

#### `start()`

Start the Φ source and begin producing bits.

#### `stop()`

Stop the Φ source.

#### `get_bits(n, timeout=5.0) → List[int]`

Get n raw bits from the buffer.

```python
bits = source.get_bits(32)
# bits: [1, 0, 1, 1, 0, 1, ...]
```

#### `get_status() → Dict`

Return the current status of the source.

```python
status = source.get_status()
# status: {
#     "running": True,
#     "buffer_size": 5000,
#     "last_phi": 0.72,
#     "source_quality": 0.95,
#     "entropy_per_bit": 0.99,
#     "total_bits_generated": 100000,
# }
```

## SamplerLoop

Transforms bits into samples.

### Constructor

```python
SamplerLoop(source, config=None)
```

### Methods

#### `sample_uniform(n, min_val, max_val) → List[float]`

Uniform samples.

#### `sample_normal(n, mean, std) → List[float]`

Normal samples.

#### `sample_exponential(n, rate) → List[float]`

Exponential samples.

#### `sample(distribution, n, **params) → List[float]`

Generic sample method.

```python
samples = sampler.sample("uniform", 10, min=0, max=1)
samples = sampler.sample("normal", 10, mean=0, std=1)
samples = sampler.sample("exponential", 10, rate=1)
```

## EleganceMonitorLoop

Quality control.

### Constructor

```python
EleganceMonitorLoop(source, sampler, test_suite=None)
```

### Methods

#### `evaluate(sample_size=1000) → EleganceMetric`

Run statistical tests and compute C/K.

```python
metric = monitor.evaluate()
print(f"Score: {metric.score:.4f}")
print(f"All tests passed: {monitor.test_suite.all_passed}")
```
