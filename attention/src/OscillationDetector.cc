/*
 * OscillationDetector.cc
 *
 * FFT-based spectral analysis of attention value time series
 * for emergent oscillation detection.
 */

#include "OscillationDetector.h"
#include <algorithm>
#include <numeric>
#include <cmath>
#include <cassert>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

namespace opencog {

OscillationDetector::OscillationDetector(const DetectorConfig& config)
    : config_(config)
{
}

OscillationDetector::~OscillationDetector() = default;

void OscillationDetector::record_sample(const std::string& entity_id,
                                         double attention_value)
{
    auto& series = time_series_[entity_id];
    series.push_back(attention_value);

    // Trim to max history
    if (series.size() > config_.max_history) {
        series.erase(series.begin(),
                     series.begin() + (series.size() - config_.max_history));
    }
}

void OscillationDetector::record_samples(const std::string& entity_id,
                                          const std::vector<double>& values)
{
    auto& series = time_series_[entity_id];
    series.insert(series.end(), values.begin(), values.end());

    if (series.size() > config_.max_history) {
        series.erase(series.begin(),
                     series.begin() + (series.size() - config_.max_history));
    }
}

OscillationResult OscillationDetector::analyze(const std::string& entity_id)
{
    OscillationResult result;
    result.entity_id = entity_id;
    result.total_spectral_power = 0.0;
    result.dominant_frequency = 0.0;
    result.oscillation_strength = 0.0;
    result.is_oscillating = false;

    auto it = time_series_.find(entity_id);
    if (it == time_series_.end() || it->second.size() < config_.min_samples) {
        return result;
    }

    const auto& raw_signal = it->second;

    // Remove DC offset (mean)
    double mean = std::accumulate(raw_signal.begin(), raw_signal.end(), 0.0) /
                  raw_signal.size();
    std::vector<double> signal(raw_signal.size());
    for (size_t i = 0; i < raw_signal.size(); ++i) {
        signal[i] = raw_signal[i] - mean;
    }

    // Apply Hann window to reduce spectral leakage
    auto windowed = apply_hann_window(signal);

    // Compute DFT
    auto dft = compute_dft(windowed);

    // Compute power spectrum
    auto power_spectrum = compute_power_spectrum(dft);

    // Total spectral power
    result.total_spectral_power = std::accumulate(
        power_spectrum.begin(), power_spectrum.end(), 0.0);

    // Find spectral peaks
    result.peaks = find_peaks(power_spectrum, config_.sampling_rate);

    // Determine dominant frequency and oscillation strength
    if (!result.peaks.empty()) {
        // Sort by power (descending)
        std::sort(result.peaks.begin(), result.peaks.end(),
                  [](const SpectralPeak& a, const SpectralPeak& b) {
                      return a.power > b.power;
                  });

        // Limit number of peaks
        if (result.peaks.size() > config_.max_peaks) {
            result.peaks.resize(config_.max_peaks);
        }

        result.dominant_frequency = result.peaks[0].frequency;

        // Oscillation strength: fraction of power in the dominant peak
        if (result.total_spectral_power > 0.0) {
            result.oscillation_strength =
                result.peaks[0].power / result.total_spectral_power;
        }
    }

    result.is_oscillating =
        result.oscillation_strength >= config_.oscillation_threshold;

    // Cache result
    last_results_[entity_id] = result;
    return result;
}

std::vector<OscillationResult> OscillationDetector::analyze_all()
{
    std::vector<OscillationResult> results;
    for (const auto& [entity_id, _] : time_series_) {
        results.push_back(analyze(entity_id));
    }
    return results;
}

PhaseRelationship OscillationDetector::compute_phase_relationship(
    const std::string& entity_a, const std::string& entity_b)
{
    PhaseRelationship rel;
    rel.entity_a = entity_a;
    rel.entity_b = entity_b;
    rel.phase_difference = 0.0;
    rel.coherence = 0.0;
    rel.is_synchronized = false;

    auto it_a = time_series_.find(entity_a);
    auto it_b = time_series_.find(entity_b);

    if (it_a == time_series_.end() || it_b == time_series_.end()) return rel;

    const auto& sig_a = it_a->second;
    const auto& sig_b = it_b->second;

    // Need same length for cross-spectrum
    size_t n = std::min(sig_a.size(), sig_b.size());
    if (n < config_.min_samples) return rel;

    // Use the last n samples from each
    std::vector<double> a(sig_a.end() - n, sig_a.end());
    std::vector<double> b(sig_b.end() - n, sig_b.end());

    // Remove DC offset
    double mean_a = std::accumulate(a.begin(), a.end(), 0.0) / n;
    double mean_b = std::accumulate(b.begin(), b.end(), 0.0) / n;
    for (size_t i = 0; i < n; ++i) {
        a[i] -= mean_a;
        b[i] -= mean_b;
    }

    // Cross-spectrum
    auto cross = compute_cross_spectrum(a, b);

    // Auto-spectra for coherence normalization
    auto dft_a = compute_dft(a);
    auto dft_b = compute_dft(b);
    auto psd_a = compute_power_spectrum(dft_a);
    auto psd_b = compute_power_spectrum(dft_b);

    // Find dominant frequency bin (peak of cross-spectrum magnitude)
    size_t dominant_bin = 0;
    double max_cross_power = 0.0;
    for (size_t i = 1; i < cross.size(); ++i) {
        double cp = std::abs(cross[i]);
        if (cp > max_cross_power) {
            max_cross_power = cp;
            dominant_bin = i;
        }
    }

    if (dominant_bin > 0 && dominant_bin < cross.size()) {
        // Phase difference at dominant frequency
        rel.phase_difference = std::arg(cross[dominant_bin]);

        // Coherence: |Sxy|^2 / (Sxx * Syy) at dominant bin
        double denom = psd_a[dominant_bin] * psd_b[dominant_bin];
        if (denom > 0.0) {
            double cross_mag_sq = std::norm(cross[dominant_bin]);
            rel.coherence = cross_mag_sq / denom;
            rel.coherence = std::min(1.0, rel.coherence);  // Clamp
        }
    }

    rel.is_synchronized = rel.coherence >= config_.coherence_threshold;
    return rel;
}

std::vector<PhaseRelationship> OscillationDetector::find_synchronized_pairs()
{
    std::vector<PhaseRelationship> pairs;
    std::vector<std::string> entity_ids;
    for (const auto& [id, _] : time_series_) {
        entity_ids.push_back(id);
    }

    for (size_t i = 0; i < entity_ids.size(); ++i) {
        for (size_t j = i + 1; j < entity_ids.size(); ++j) {
            auto rel = compute_phase_relationship(entity_ids[i], entity_ids[j]);
            if (rel.is_synchronized) {
                pairs.push_back(rel);
            }
        }
    }
    return pairs;
}

size_t OscillationDetector::get_sample_count(const std::string& entity_id) const
{
    auto it = time_series_.find(entity_id);
    if (it != time_series_.end()) return it->second.size();
    return 0;
}

void OscillationDetector::clear(const std::string& entity_id)
{
    if (entity_id.empty()) {
        time_series_.clear();
        last_results_.clear();
    } else {
        time_series_.erase(entity_id);
        last_results_.erase(entity_id);
    }
}

// -- Private methods --

std::vector<std::complex<double>> OscillationDetector::compute_dft(
    const std::vector<double>& signal) const
{
    size_t N = signal.size();
    std::vector<std::complex<double>> result(N / 2 + 1);

    for (size_t k = 0; k <= N / 2; ++k) {
        std::complex<double> sum(0.0, 0.0);
        for (size_t n = 0; n < N; ++n) {
            double angle = -2.0 * M_PI * k * n / N;
            sum += signal[n] * std::complex<double>(std::cos(angle), std::sin(angle));
        }
        result[k] = sum / static_cast<double>(N);
    }
    return result;
}

std::vector<double> OscillationDetector::compute_power_spectrum(
    const std::vector<std::complex<double>>& dft) const
{
    std::vector<double> power(dft.size());
    for (size_t i = 0; i < dft.size(); ++i) {
        power[i] = std::norm(dft[i]);  // |z|^2
    }
    return power;
}

std::vector<SpectralPeak> OscillationDetector::find_peaks(
    const std::vector<double>& power_spectrum,
    double sampling_rate) const
{
    std::vector<SpectralPeak> peaks;
    if (power_spectrum.size() < 3) return peaks;

    // Find the maximum power for relative threshold
    double max_power = *std::max_element(
        power_spectrum.begin() + 1, power_spectrum.end());
    double threshold = max_power * config_.peak_threshold;

    size_t N = (power_spectrum.size() - 1) * 2;  // Original signal length
    double freq_resolution = sampling_rate / N;

    // Simple peak detection: local maxima above threshold
    for (size_t i = 1; i < power_spectrum.size() - 1; ++i) {
        if (power_spectrum[i] > power_spectrum[i-1] &&
            power_spectrum[i] > power_spectrum[i+1] &&
            power_spectrum[i] >= threshold) {

            SpectralPeak peak;
            peak.frequency = i * freq_resolution;
            peak.power = power_spectrum[i];
            peak.amplitude = std::sqrt(power_spectrum[i]);

            // Phase from DFT (we don't have it here, approximate as 0)
            peak.phase = 0.0;

            // Estimate bandwidth using -3dB points
            double half_power = power_spectrum[i] / 2.0;
            size_t left = i, right = i;
            while (left > 0 && power_spectrum[left] > half_power) left--;
            while (right < power_spectrum.size() - 1 &&
                   power_spectrum[right] > half_power) right++;
            peak.bandwidth = (right - left) * freq_resolution;

            peaks.push_back(peak);
        }
    }

    return peaks;
}

std::vector<std::complex<double>> OscillationDetector::compute_cross_spectrum(
    const std::vector<double>& signal_a,
    const std::vector<double>& signal_b) const
{
    auto dft_a = compute_dft(signal_a);
    auto dft_b = compute_dft(signal_b);

    size_t n = std::min(dft_a.size(), dft_b.size());
    std::vector<std::complex<double>> cross(n);

    for (size_t i = 0; i < n; ++i) {
        // Cross-spectrum: Sxy = X* · Y (conjugate of X times Y)
        cross[i] = std::conj(dft_a[i]) * dft_b[i];
    }

    return cross;
}

std::vector<double> OscillationDetector::apply_hann_window(
    const std::vector<double>& signal) const
{
    size_t N = signal.size();
    std::vector<double> windowed(N);
    for (size_t n = 0; n < N; ++n) {
        double w = 0.5 * (1.0 - std::cos(2.0 * M_PI * n / (N - 1)));
        windowed[n] = signal[n] * w;
    }
    return windowed;
}

} // namespace opencog
