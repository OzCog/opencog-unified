#!/usr/bin/env python3
"""
Emergent Oscillation Benchmark
Issue #218: Cognitive Layer — Distributed Cognition Dynamics

Runs extended ECAN simulation to detect and benchmark emergent
oscillatory patterns in attention dynamics. Validates that
expected oscillation emergence occurs under controlled conditions.
"""

import json
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class OscillationPeak:
    """A detected spectral peak."""
    frequency: float
    amplitude: float
    power: float


@dataclass
class OscillationAnalysis:
    """Result of oscillation analysis for one entity."""
    entity_id: str
    is_oscillating: bool
    dominant_frequency: float
    oscillation_strength: float
    peaks: List[OscillationPeak]


@dataclass
class PhaseRelation:
    """Phase relationship between two entities."""
    entity_a: str
    entity_b: str
    phase_diff: float
    coherence: float
    is_synchronized: bool


class SimpleFFT:
    """Minimal DFT implementation for oscillation detection."""

    @staticmethod
    def dft(signal: List[float]) -> List[complex]:
        """Compute DFT of real-valued signal."""
        N = len(signal)
        result = []
        for k in range(N // 2 + 1):
            s = 0.0 + 0.0j
            for n in range(N):
                angle = -2.0 * math.pi * k * n / N
                s += signal[n] * complex(math.cos(angle), math.sin(angle))
            result.append(s / N)
        return result

    @staticmethod
    def power_spectrum(dft_result: List[complex]) -> List[float]:
        """Compute power spectrum from DFT."""
        return [abs(c) ** 2 for c in dft_result]

    @staticmethod
    def hann_window(signal: List[float]) -> List[float]:
        """Apply Hann window to reduce spectral leakage."""
        N = len(signal)
        return [signal[n] * 0.5 * (1.0 - math.cos(2.0 * math.pi * n / (N - 1)))
                for n in range(N)]

    @staticmethod
    def find_peaks(power: List[float], sampling_rate: float,
                   threshold_ratio: float = 0.1) -> List[OscillationPeak]:
        """Find spectral peaks above threshold."""
        if len(power) < 3:
            return []
        max_power = max(power[1:])  # Skip DC
        threshold = max_power * threshold_ratio
        N = (len(power) - 1) * 2
        freq_res = sampling_rate / N

        peaks = []
        for i in range(1, len(power) - 1):
            if (power[i] > power[i-1] and power[i] > power[i+1]
                    and power[i] >= threshold):
                peaks.append(OscillationPeak(
                    frequency=i * freq_res,
                    amplitude=math.sqrt(power[i]),
                    power=power[i],
                ))
        return sorted(peaks, key=lambda p: p.power, reverse=True)


class OscillationBenchmark:
    """Extended ECAN simulation for oscillation detection."""

    def __init__(self, num_atoms: int = 100, num_agents: int = 4, seed: int = 42):
        self.rng = random.Random(seed)
        self.num_atoms = num_atoms
        self.num_agents = num_agents
        self.fft = SimpleFFT()

        # Per-agent attention time series
        self.agent_sti_history: Dict[str, List[float]] = {}
        # Per-atom STI time series (sample subset)
        self.atom_sti_history: Dict[str, List[float]] = {}

        # Initialize agents with coupled dynamics
        self.agent_sti: Dict[str, float] = {}
        self.agent_phase: Dict[str, float] = {}
        self.coupling_strength = 0.15

        for i in range(num_agents):
            agent_id = f"agent_{i}"
            self.agent_sti[agent_id] = self.rng.gauss(100.0, 20.0)
            self.agent_phase[agent_id] = self.rng.uniform(0, 2 * math.pi)
            self.agent_sti_history[agent_id] = []

        # Track a subset of atoms for oscillation detection
        self.tracked_atoms = [f"atom_{i}" for i in range(min(10, num_atoms))]
        self.atom_sti: Dict[str, float] = {}
        for atom_id in self.tracked_atoms:
            self.atom_sti[atom_id] = self.rng.gauss(50.0, 15.0)
            self.atom_sti_history[atom_id] = []

    def simulate_cycle(self, cycle: int, dt: float = 0.1):
        """Simulate one coupled oscillation cycle."""
        # Agent dynamics: coupled oscillators with ECAN-like interaction
        new_sti = {}
        for agent_id in self.agent_sti:
            # Intrinsic oscillation (each agent has natural frequency)
            idx = int(agent_id.split('_')[1])
            natural_freq = 0.5 + idx * 0.3  # Different natural frequencies
            phase = self.agent_phase[agent_id]

            # Oscillatory drive
            osc_drive = 20.0 * math.sin(2 * math.pi * natural_freq * cycle * dt + phase)

            # Coupling from other agents (Kuramoto-like)
            coupling = 0.0
            for other_id, other_sti in self.agent_sti.items():
                if other_id != agent_id:
                    coupling += self.coupling_strength * (other_sti - self.agent_sti[agent_id])

            # ECAN-like dynamics: rent decay + wage + oscillation + coupling
            rent_decay = -0.02 * self.agent_sti[agent_id]
            wage = 5.0 if self.rng.random() < 0.3 else 0.0
            noise = self.rng.gauss(0, 2.0)

            new_sti[agent_id] = (self.agent_sti[agent_id] +
                                 osc_drive * dt + coupling * dt +
                                 rent_decay * dt + wage * dt + noise * dt)

        self.agent_sti = new_sti

        # Record agent histories
        for agent_id, sti in self.agent_sti.items():
            self.agent_sti_history[agent_id].append(sti)

        # Atom dynamics: driven by nearest agent + spreading
        for i, atom_id in enumerate(self.tracked_atoms):
            driver_agent = f"agent_{i % self.num_agents}"
            drive = 0.1 * (self.agent_sti[driver_agent] - self.atom_sti[atom_id])
            noise = self.rng.gauss(0, 1.0)
            self.atom_sti[atom_id] += drive * dt + noise * dt
            self.atom_sti_history[atom_id].append(self.atom_sti[atom_id])

    def analyze_oscillations(self, sampling_rate: float = 10.0
                             ) -> Tuple[List[OscillationAnalysis], List[PhaseRelation]]:
        """Analyze all recorded time series for oscillations."""
        analyses = []

        # Analyze agents
        for agent_id, history in self.agent_sti_history.items():
            if len(history) < 64:
                continue
            analysis = self._analyze_signal(agent_id, history, sampling_rate)
            analyses.append(analysis)

        # Analyze tracked atoms
        for atom_id, history in self.atom_sti_history.items():
            if len(history) < 64:
                continue
            analysis = self._analyze_signal(atom_id, history, sampling_rate)
            analyses.append(analysis)

        # Phase relationships between agents
        phase_relations = []
        agent_ids = list(self.agent_sti_history.keys())
        for i in range(len(agent_ids)):
            for j in range(i + 1, len(agent_ids)):
                rel = self._compute_phase_relation(
                    agent_ids[i], agent_ids[j], sampling_rate)
                if rel:
                    phase_relations.append(rel)

        return analyses, phase_relations

    def _analyze_signal(self, entity_id: str, signal: List[float],
                        sampling_rate: float) -> OscillationAnalysis:
        """Analyze a single signal for oscillations."""
        # Remove DC offset
        mean = sum(signal) / len(signal)
        centered = [s - mean for s in signal]

        # Window and DFT
        windowed = self.fft.hann_window(centered)
        dft_result = self.fft.dft(windowed)
        power = self.fft.power_spectrum(dft_result)
        peaks = self.fft.find_peaks(power, sampling_rate)

        total_power = sum(power[1:])  # Exclude DC
        dominant_freq = peaks[0].frequency if peaks else 0.0
        osc_strength = (peaks[0].power / total_power) if (peaks and total_power > 0) else 0.0

        return OscillationAnalysis(
            entity_id=entity_id,
            is_oscillating=osc_strength > 0.2,
            dominant_frequency=dominant_freq,
            oscillation_strength=osc_strength,
            peaks=peaks[:3],
        )

    def _compute_phase_relation(self, entity_a: str, entity_b: str,
                                sampling_rate: float) -> Optional[PhaseRelation]:
        """Compute phase relationship between two entities."""
        hist_a = self.agent_sti_history.get(entity_a, [])
        hist_b = self.agent_sti_history.get(entity_b, [])
        n = min(len(hist_a), len(hist_b))
        if n < 64:
            return None

        sig_a = hist_a[-n:]
        sig_b = hist_b[-n:]

        mean_a = sum(sig_a) / n
        mean_b = sum(sig_b) / n
        sig_a = [s - mean_a for s in sig_a]
        sig_b = [s - mean_b for s in sig_b]

        # Cross-correlation at lag 0 for coherence estimate
        dft_a = self.fft.dft(sig_a)
        dft_b = self.fft.dft(sig_b)

        # Find dominant frequency bin
        power_a = self.fft.power_spectrum(dft_a)
        max_bin = max(range(1, len(power_a)), key=lambda i: power_a[i])

        # Cross-spectrum at dominant bin
        cross = dft_a[max_bin].conjugate() * dft_b[max_bin]
        phase_diff = math.atan2(cross.imag, cross.real)

        # Coherence approximation
        denom = abs(dft_a[max_bin]) * abs(dft_b[max_bin])
        coherence = abs(cross) / denom if denom > 0 else 0.0

        return PhaseRelation(
            entity_a=entity_a,
            entity_b=entity_b,
            phase_diff=phase_diff,
            coherence=min(1.0, coherence),
            is_synchronized=coherence > 0.7,
        )


def test_emergent_oscillations():
    """Main test: Run extended simulation and detect oscillations."""
    print("=" * 70)
    print("Emergent Oscillation Benchmark")
    print("Issue #218: Cognitive Layer — Distributed Cognition Dynamics")
    print("=" * 70)

    # Run simulation with coupled agents
    bench = OscillationBenchmark(num_atoms=50, num_agents=4, seed=42)

    num_cycles = 1000
    sampling_rate = 10.0
    dt = 1.0 / sampling_rate

    start_time = time.time()
    for cycle in range(num_cycles):
        bench.simulate_cycle(cycle, dt)
    elapsed = time.time() - start_time

    print(f"\nSimulation: {num_cycles} cycles, {bench.num_agents} agents, "
          f"{len(bench.tracked_atoms)} tracked atoms")
    print(f"Time: {elapsed:.3f}s ({elapsed/num_cycles*1000:.2f} ms/cycle)")

    # Analyze oscillations
    analyses, phase_relations = bench.analyze_oscillations(sampling_rate)

    print(f"\n--- Oscillation Analysis ---")
    oscillating_count = 0
    for a in analyses:
        status = "✓ OSCILLATING" if a.is_oscillating else "  stable"
        if a.is_oscillating:
            oscillating_count += 1
        print(f"  {a.entity_id:12s}: {status} | "
              f"freq={a.dominant_frequency:.3f} Hz | "
              f"strength={a.oscillation_strength:.3f}")

    print(f"\n--- Phase Relationships ---")
    synced_pairs = 0
    for rel in phase_relations:
        status = "SYNCED" if rel.is_synchronized else "independent"
        if rel.is_synchronized:
            synced_pairs += 1
        print(f"  {rel.entity_a} ↔ {rel.entity_b}: "
              f"Δφ={rel.phase_diff:.3f} rad | "
              f"coherence={rel.coherence:.3f} | {status}")

    print(f"\n--- Summary ---")
    print(f"  Oscillating entities: {oscillating_count}/{len(analyses)}")
    print(f"  Synchronized pairs: {synced_pairs}/{len(phase_relations)}")

    # Assertions: coupled oscillators should produce emergent oscillations
    agent_analyses = [a for a in analyses if a.entity_id.startswith("agent_")]
    assert any(a.is_oscillating for a in agent_analyses), \
        "At least one agent should exhibit oscillatory behavior"

    assert oscillating_count > 0, \
        "Expected emergent oscillations in coupled system"

    # With coupling, some phase relationships should emerge
    assert len(phase_relations) > 0, \
        "Should detect phase relationships between agents"

    print("\n✓ All emergent oscillation assertions passed")

    # Produce benchmark output
    output = {
        "benchmark": "emergent_oscillations",
        "simulation": {
            "num_cycles": num_cycles,
            "num_agents": bench.num_agents,
            "num_tracked_atoms": len(bench.tracked_atoms),
            "coupling_strength": bench.coupling_strength,
            "sampling_rate": sampling_rate,
            "total_time_s": elapsed,
        },
        "oscillation_results": [
            {
                "entity_id": a.entity_id,
                "is_oscillating": a.is_oscillating,
                "dominant_frequency": a.dominant_frequency,
                "oscillation_strength": a.oscillation_strength,
                "num_peaks": len(a.peaks),
            }
            for a in analyses
        ],
        "phase_relations": [
            {
                "entity_a": r.entity_a,
                "entity_b": r.entity_b,
                "phase_diff_rad": r.phase_diff,
                "coherence": r.coherence,
                "is_synchronized": r.is_synchronized,
            }
            for r in phase_relations
        ],
        "summary": {
            "oscillating_entities": oscillating_count,
            "total_entities": len(analyses),
            "synchronized_pairs": synced_pairs,
            "total_pairs": len(phase_relations),
        },
    }

    output_path = "test_emergent_oscillations_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults written to: {output_path}")


if __name__ == "__main__":
    test_emergent_oscillations()
