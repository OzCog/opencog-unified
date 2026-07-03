/*
 * SharedHypergraphContext.cc
 *
 * Implementation of shared hypergraph context for agent synchronization.
 */

#include "SharedHypergraphContext.h"
#include <algorithm>
#include <numeric>
#include <cmath>

namespace opencog {

SharedHypergraphContext::SharedHypergraphContext()
    : context_version_(0)
{
}

SharedHypergraphContext::~SharedHypergraphContext() = default;

void SharedHypergraphContext::update_hypergraph_node(
    const std::string& node_id, const std::vector<double>& node_state)
{
    std::unique_lock<std::shared_mutex> lock(context_mutex_);
    hypergraph_nodes_[node_id] = node_state;
    context_version_++;
}

void SharedHypergraphContext::update_hypergraph_edge(
    const std::string& edge_id,
    const std::vector<std::string>& connected_nodes,
    const std::vector<double>& edge_weights)
{
    std::unique_lock<std::shared_mutex> lock(context_mutex_);
    hypergraph_edges_[edge_id] = std::make_pair(connected_nodes, edge_weights);
    context_version_++;
}

void SharedHypergraphContext::update_agent_state(
    const std::string& agent_id, const std::vector<double>& agent_state)
{
    std::unique_lock<std::shared_mutex> lock(context_mutex_);
    agent_states_[agent_id] = agent_state;
    last_update_times_[agent_id] = std::chrono::steady_clock::now();
    context_version_++;
}

std::vector<double> SharedHypergraphContext::get_hypergraph_node(
    const std::string& node_id) const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);
    auto it = hypergraph_nodes_.find(node_id);
    if (it != hypergraph_nodes_.end()) {
        return it->second;
    }
    return {};
}

std::pair<std::vector<std::string>, std::vector<double>>
SharedHypergraphContext::get_hypergraph_edge(const std::string& edge_id) const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);
    auto it = hypergraph_edges_.find(edge_id);
    if (it != hypergraph_edges_.end()) {
        return it->second;
    }
    return {{}, {}};
}

std::vector<double> SharedHypergraphContext::get_agent_state(
    const std::string& agent_id) const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);
    auto it = agent_states_.find(agent_id);
    if (it != agent_states_.end()) {
        return it->second;
    }
    return {};
}

std::map<std::string, std::vector<double>>
SharedHypergraphContext::get_all_agent_states() const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);
    return agent_states_;
}

std::vector<double> SharedHypergraphContext::get_aggregated_context() const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);
    return compute_aggregated_state();
}

bool SharedHypergraphContext::synchronize_context(
    const std::map<std::string, std::vector<double>>& external_updates)
{
    std::unique_lock<std::shared_mutex> lock(context_mutex_);

    for (const auto& [key, values] : external_updates) {
        // Merge with existing state using weighted average
        auto it = hypergraph_nodes_.find(key);
        if (it != hypergraph_nodes_.end()) {
            auto& existing = it->second;
            size_t min_size = std::min(existing.size(), values.size());
            for (size_t i = 0; i < min_size; ++i) {
                existing[i] = existing[i] * 0.7 + values[i] * 0.3;
            }
        } else {
            hypergraph_nodes_[key] = values;
        }
    }

    context_version_++;
    return true;
}

void SharedHypergraphContext::cleanup_stale_states(double timeout_seconds)
{
    std::unique_lock<std::shared_mutex> lock(context_mutex_);
    auto now = std::chrono::steady_clock::now();

    std::vector<std::string> stale_agents;
    for (const auto& [agent_id, update_time] : last_update_times_) {
        auto elapsed = std::chrono::duration<double>(now - update_time).count();
        if (elapsed > timeout_seconds) {
            stale_agents.push_back(agent_id);
        }
    }

    for (const auto& agent_id : stale_agents) {
        agent_states_.erase(agent_id);
        last_update_times_.erase(agent_id);
    }

    if (!stale_agents.empty()) {
        context_version_++;
    }
}

SharedHypergraphContext::ContextStats
SharedHypergraphContext::get_context_statistics() const
{
    std::shared_lock<std::shared_mutex> lock(context_mutex_);

    ContextStats stats;
    stats.num_nodes = hypergraph_nodes_.size();
    stats.num_edges = hypergraph_edges_.size();
    stats.num_agents = agent_states_.size();
    stats.version = context_version_.load();

    // Compute average update frequency
    if (last_update_times_.empty()) {
        stats.avg_update_frequency = 0.0;
    } else {
        auto now = std::chrono::steady_clock::now();
        double total_elapsed = 0.0;
        for (const auto& [_, update_time] : last_update_times_) {
            total_elapsed += std::chrono::duration<double>(now - update_time).count();
        }
        stats.avg_update_frequency = static_cast<double>(last_update_times_.size()) /
                                     (total_elapsed / last_update_times_.size());
    }

    return stats;
}

std::vector<double> SharedHypergraphContext::compute_aggregated_state() const
{
    // Aggregate all node and agent states into a single context vector
    // using mean-pooling with dimensionality reduction
    const size_t target_dim = 32;
    std::vector<double> aggregated(target_dim, 0.0);
    size_t count = 0;

    // Aggregate hypergraph node states
    for (const auto& [_, node_state] : hypergraph_nodes_) {
        for (size_t i = 0; i < node_state.size() && i < target_dim; ++i) {
            aggregated[i] += node_state[i];
        }
        count++;
    }

    // Aggregate agent states
    for (const auto& [_, agent_state] : agent_states_) {
        for (size_t i = 0; i < agent_state.size() && i < target_dim; ++i) {
            aggregated[i] += agent_state[i];
        }
        count++;
    }

    // Normalize
    if (count > 0) {
        for (auto& val : aggregated) {
            val /= static_cast<double>(count);
        }
    }

    return aggregated;
}

} // namespace opencog
