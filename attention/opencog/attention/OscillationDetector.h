/*
 * OscillationDetector.h
 *
 * Detects emergent oscillation patterns in attention value time series.
 * Uses spectral analysis (DFT) to identify dominant frequencies, amplitudes,
 * and phase relationships in ECAN attention dynamics.
 */

#ifndef _OPENCOG_OSCILLATION_DETECTOR_H
#define _OPENCOG_OSCILLATION_DETECTOR_H

#include <vector>
#include <string>
#include <map>
#include <complex>
#include <cstdint>

namespace opencog {

/**
 * Spectral peak detected in the attention time series.
 */
struct SpectralPeak {
    double frequency;      // Dominant frequency (Hz or cycles/sample)
    double amplitude;      // Peak amplitude
    double phase;          // Phase angle (radians)
    double power;          // Spectral power (amplitude^2)
    double bandwidth;      // Width of the peak at -3dB
};

/**
 * Result of oscillation analysis for a single atom/agent.
 */
struct OscillationResult {
    std::string entity_id;
    std::vector<SpectralPeak> peaks;
    double total_spectral_power;
    double dominant_frequency;
    double oscillation_strength;  // 0.0 = no oscillation, 1.0 = pure sine
    bool is_oscillating;          // True if clear oscillation detected
};

/**
 * Phase relationship between two oscillating entities.
 */
struct PhaseRelationship {
    std::string entity_a;
    std::string entity_b;
    double phase_difference;    // radians
    double coherence;           // [0,1] how stable the phase relationship is
    bool is_synchronized;       // True if phase-locked
};

/**
 * OscillationDetector
 *
 * Analyzes attention value time series for emergent oscillatory patterns.
 * Uses Discrete Fourier Transform (DFT) for spectral analysis.
 */
class OscillationDetector
{
public:
    struct DetectorConfig {
        size_t min_samples = 64;            // Minimum samples for analysis
        size_t max_history = 1024;          // Maximum time series length
        double sampling_rate = 10.0;        // Samples per second
        double peak_threshold = 0.1;        // Minimum relative amplitude for peak detection
        double oscillation_threshold = 0.3; // Min oscillation_strength to flag as oscillating
        double coherence_threshold = 0.7;   // Min coherence for phase-lock detection
        size_t max_peaks = 5;               // Maximum peaks to report per entity
    };

private:
    DetectorConfig config_;
    // Time series buffer: entity_id -> sequence of attention values
    std::map<std::string, std::vector<double>> time_series_;
    // Last analysis results cache
    std::map<std::string, OscillationResult> last_results_;

public:
    explicit OscillationDetector(const DetectorConfig& config = DetectorConfig());
    ~OscillationDetector();

    /**
     * Record an attention value sample for an entity.
     */
    void record_sample(const std::string& entity_id, double attention_value);

    /**
     * Record batch of samples for an entity.
     */
    void record_samples(const std::string& entity_id,
                        const std::vector<double>& values);

    /**
     * Analyze oscillation patterns for a specific entity.
     * Requires at least min_samples recorded values.
     */
    OscillationResult analyze(const std::string& entity_id);

    /**
     * Analyze all recorded entities.
     */
    std::vector<OscillationResult> analyze_all();

    /**
     * Compute phase relationships between two entities.
     */
    PhaseRelationship compute_phase_relationship(
        const std::string& entity_a,
        const std::string& entity_b);

    /**
     * Find all phase-locked pairs among recorded entities.
     */
    std::vector<PhaseRelationship> find_synchronized_pairs();

    /**
     * Get the number of samples recorded for an entity.
     */
    size_t get_sample_count(const std::string& entity_id) const;

    /**
     * Clear recorded data for an entity or all entities.
     */
    void clear(const std::string& entity_id = "");

    /**
     * Get detector configuration.
     */
    const DetectorConfig& get_config() const { return config_; }

private:
    /**
     * Compute DFT of a real-valued time series.
     */
    std::vector<std::complex<double>> compute_dft(
        const std::vector<double>& signal) const;

    /**
     * Compute power spectrum from DFT result.
     */
    std::vector<double> compute_power_spectrum(
        const std::vector<std::complex<double>>& dft) const;

    /**
     * Find spectral peaks in power spectrum.
     */
    std::vector<SpectralPeak> find_peaks(
        const std::vector<double>& power_spectrum,
        double sampling_rate) const;

    /**
     * Compute cross-spectral density between two signals.
     */
    std::vector<std::complex<double>> compute_cross_spectrum(
        const std::vector<double>& signal_a,
        const std::vector<double>& signal_b) const;

    /**
     * Apply Hann window to reduce spectral leakage.
     */
    std::vector<double> apply_hann_window(
        const std::vector<double>& signal) const;
};

} // namespace opencog

#endif // _OPENCOG_OSCILLATION_DETECTOR_H
