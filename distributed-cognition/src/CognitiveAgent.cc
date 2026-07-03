/*
 * CognitiveAgent.cc
 *
 * Implementation of the CognitiveAgent class for distributed cognition.
 */

#include "CognitiveAgent.h"
#include <algorithm>
#include <numeric>
#include <cmath>
#include <chrono>

namespace opencog {

CognitiveAgent::CognitiveAgent(const std::string& id, double frequency, int max_iterations)
    : agent_id_(id),
      active_(false),
      processing_(false),
      cycle_frequency_(frequency),
      max_cycle_iterations_(max_iterations)
{
    internal_state_.resize(16, 0.0);
}

CognitiveAgent::~CognitiveAgent()
{
    stop_cognitive_cycle();
}

void CognitiveAgent::start_cognitive_cycle()
{
    if (active_.load()) return;
    active_.store(true);
    cognitive_thread_ = std::make_unique<std::thread>(
        &CognitiveAgent::cognitive_processing_loop, this);
}

void CognitiveAgent::stop_cognitive_cycle()
{
    active_.store(false);
    cycle_cv_.notify_all();
    if (cognitive_thread_ && cognitive_thread_->joinable()) {
        cognitive_thread_->join();
    }
    cognitive_thread_.reset();
}

std::vector<double> CognitiveAgent::cognitive_iteration(
    const std::vector<double>& shared_context)
{
    std::lock_guard<std::mutex> lock(state_mutex_);
    processing_.store(true);

    // Combine agent inputs with shared context
    std::vector<double> combined_inputs = input_from_agents_;
    combined_inputs.insert(combined_inputs.end(),
                          shared_context.begin(), shared_context.end());

    // Process cognitive inputs
    auto output = process_cognitive_inputs(combined_inputs);

    // Apply learning from processing results
    apply_cognitive_learning(output);

    // Store output for distribution
    output_to_agents_ = output;
    processing_.store(false);
    return output;
}

void CognitiveAgent::receive_agent_input(const std::string& agent_id,
                                          const std::vector<double>& input_data)
{
    std::lock_guard<std::mutex> lock(state_mutex_);
    // Accumulate inputs — weighted sum with existing
    if (input_from_agents_.empty()) {
        input_from_agents_ = input_data;
    } else {
        size_t min_size = std::min(input_from_agents_.size(), input_data.size());
        for (size_t i = 0; i < min_size; ++i) {
            input_from_agents_[i] += input_data[i] * 0.5;
        }
    }
}

void CognitiveAgent::add_adjacent_agent(const std::string& agent_id)
{
    std::lock_guard<std::mutex> lock(state_mutex_);
    if (std::find(adjacent_agents_.begin(), adjacent_agents_.end(), agent_id)
        == adjacent_agents_.end()) {
        adjacent_agents_.push_back(agent_id);
    }
}

void CognitiveAgent::update_internal_state(const std::vector<double>& state_updates)
{
    std::lock_guard<std::mutex> lock(state_mutex_);
    size_t min_size = std::min(internal_state_.size(), state_updates.size());
    for (size_t i = 0; i < min_size; ++i) {
        internal_state_[i] += state_updates[i];
    }
}

std::vector<double> CognitiveAgent::get_cognitive_state() const
{
    // Note: const method, but we need a lock for thread safety
    // Using const_cast pattern for mutable mutex
    auto* self = const_cast<CognitiveAgent*>(this);
    std::lock_guard<std::mutex> lock(self->state_mutex_);
    return internal_state_;
}

void CognitiveAgent::cognitive_processing_loop()
{
    auto cycle_duration = std::chrono::duration<double>(1.0 / cycle_frequency_);
    int iteration = 0;

    while (active_.load() && iteration < max_cycle_iterations_) {
        auto cycle_start = std::chrono::steady_clock::now();

        // Perform one cognitive iteration with empty shared context
        std::vector<double> empty_context;
        cognitive_iteration(empty_context);

        // Clear consumed inputs
        {
            std::lock_guard<std::mutex> lock(state_mutex_);
            input_from_agents_.clear();
        }

        iteration++;

        // Sleep for remaining cycle time
        auto elapsed = std::chrono::steady_clock::now() - cycle_start;
        auto remaining = cycle_duration - elapsed;
        if (remaining.count() > 0) {
            std::unique_lock<std::mutex> lock(state_mutex_);
            cycle_cv_.wait_for(lock, remaining, [this]() { return !active_.load(); });
        }
    }
}

std::vector<double> CognitiveAgent::process_cognitive_inputs(
    const std::vector<double>& inputs)
{
    // Sigmoid-based activation of internal state by inputs
    std::vector<double> output(internal_state_.size(), 0.0);

    for (size_t i = 0; i < internal_state_.size(); ++i) {
        double activation = internal_state_[i];

        // Integrate relevant inputs
        if (i < inputs.size()) {
            activation += inputs[i] * 0.3;
        }

        // Apply sigmoid nonlinearity for bounded dynamics
        double sigmoid = 1.0 / (1.0 + std::exp(-activation));
        output[i] = sigmoid - 0.5;  // Center around zero

        // Update internal state with decay
        internal_state_[i] = internal_state_[i] * 0.95 + output[i] * 0.1;
    }

    return output;
}

void CognitiveAgent::apply_cognitive_learning(const std::vector<double>& feedback)
{
    // Hebbian-style learning: strengthen active connections
    double learning_rate = 0.01;
    for (size_t i = 0; i < internal_state_.size() && i < feedback.size(); ++i) {
        // Simple Hebbian rule: delta_w = lr * pre * post
        double pre = internal_state_[i];
        double post = feedback[i];
        internal_state_[i] += learning_rate * pre * post;

        // Bounded normalization to prevent saturation
        internal_state_[i] = std::max(-10.0, std::min(10.0, internal_state_[i]));
    }
}

} // namespace opencog
