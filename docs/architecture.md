# Φ‑Generator Architecture

## Overview

The Φ‑Generator is a self‑improving randomness generator consisting of
three LoopObjects arranged in a pipeline:

Each component follows the LoopOS pattern with:

- `observe` – derive metrics from state and input
- `control` – decide on action
- `evaluate` – compute elegance C/K
- `mutate` – propose and apply changes
- `termination_condition` – when to stop

## Component Details

### PhiSourceLoop

The physical entropy source.

**In simulation:** uses a chaotic map to emulate Φ field fluctuations.

**In production:** interfaces with physical sensors:
- Qubit decoherence time
- EEG noise
- Network jitter
- Clock drift

**State:**
- `raw_bitstream`: circular buffer of raw bits
- `last_phi`: last measured Φ value
- `source_quality`: current quality estimate
- `entropy_per_bit`: running entropy estimate

**Mutation:** adjusts throttle rate and bit extraction to optimize
entropy per unit of computational cost.

### SamplerLoop

Transforms raw bits into samples from target distributions.

**Methods:**
- `sample_uniform(n, min_val, max_val)` – via inverse CDF
- `sample_normal(n, mean, std)` – via Box‑Muller transform
- `sample_exponential(n, rate)` – via inverse CDF

**State:**
- `output_queue`: generated samples
- `consumed_bits_per_sample`: efficiency metric
- `total_samples_generated`: cumulative count

**Mutation:** adjusts bits per sample based on elegance.

### EleganceMonitorLoop

Runs statistical tests and computes the C/K ratio.

**Tests:**
- Chi‑square test for uniformity
- Autocorrelation test
- Entropy test
- Kolmogorov‑Smirnov test

**State:**
- `elegance_score`: current C/K
- `history`: rolling history of elegance scores
- `test_results`: latest statistical test results

**Mutation:** triggers mutations in source and sampler when elegance
degrades.

## Data Flow

```
Source Reading → Bits → Uniform [0,1] → Target Distribution → Sample
     ↓                                              ↓
   Φ field                                   Elegance C/K
```

## Self‑Improvement Loop

```
Observe → Evaluate → Propose → Validate → Simulate → Commit
    ↑                                        ↓
    └────────────── Feedback ◄───────────────┘
```

The generator monitors its own elegance and mutates its parameters when
quality degrades. This closed loop follows the same principle that
drives the evolution of the universe: minimize C/K.

## Scaling

The architecture is designed to scale:

- **Single instance:** all three components run in one process
- **Multiple sources:** additional PhiSourceLoops can be added for
  increased entropy
- **Distributed:** components communicate via gRPC or message queues
- **Hardware accelerated:** the sampler can run on Φ‑Fabric tiles
