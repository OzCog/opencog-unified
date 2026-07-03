/*
 * AgentCoordinator.cc
 *
 * Implementation of agent coordination for distributed cognitive processing.
 */

#include "AgentCoordinator.h"
#include <algorithm>

namespace opencog {

AgentCoordinator::AgentCoordinator(size_t max_agents, double sync_interval_ms)
    : shared_context_(std::make_shared<SharedHypergraphContext>()),
      running_(false),
      cycle_count_(0),
      sync_interval_ms_(sync_interval_ms),
      max_agents_(max_agents)
{
}

AgentCoordinator::~AgentCoordinator()
{
    stop_all_agents();
}

bool AgentCoordinator::register_agent(std::shared_ptr<CognitiveAgent> agent)
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    if (agents_.size() >= max_agents_) return false;

    const std::string& id = agent->get_agent_id();
    if (agents_.find(id) != agents_.end()) return false;

    agents_[id] = agent;
    return true;
}

bool AgentCoordinator::unregister_agent(const std::string& agent_id)
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    auto it = agents_.find(agent_id);
    if (it == agents_.end()) return false;

    it->second->stop_cognitive_cycle();
    agents_.erase(it);
    return true;
}

void AgentCoordinator::start_all_agents()
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    running_.store(true);

    for (auto& [id, agent] : agents_) {
        agent->start_cognitive_cycle();
    }
}

void AgentCoordinator::stop_all_agents()
{
    running_.store(false);
    std::lock_guard<std::mutex> lock(coordinator_mutex_);

    for (auto& [id, agent] : agents_) {
        agent->stop_cognitive_cycle();
    }
}

void AgentCoordinator::coordination_cycle()
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);

    // Phase 1: Gather all agent states into shared context
    for (const auto& [id, agent] : agents_) {
        auto state = agent->get_cognitive_state();
        shared_context_->update_agent_state(id, state);
    }

    // Phase 2: Compute aggregated context
    auto aggregated = shared_context_->get_aggregated_context();

    // Phase 3: Distribute aggregated context to all agents as cognitive input
    for (auto& [id, agent] : agents_) {
        agent->cognitive_iteration(aggregated);
    }

    // Phase 4: Route inter-agent messages based on adjacency
    for (const auto& [id, agent] : agents_) {
        auto adjacent = agent->get_adjacent_agents();
        auto output_state = agent->get_cognitive_state();

        for (const auto& target_id : adjacent) {
            auto target_it = agents_.find(target_id);
            if (target_it != agents_.end()) {
                target_it->second->receive_agent_input(id, output_state);
            }
        }
    }

    // Phase 5: Cleanup stale states
    shared_context_->cleanup_stale_states(30.0);

    cycle_count_++;
}

void AgentCoordinator::route_message(const std::string& from_agent,
                                      const std::string& to_agent,
                                      const std::vector<double>& message)
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    auto it = agents_.find(to_agent);
    if (it != agents_.end()) {
        it->second->receive_agent_input(from_agent, message);
    }
}

void AgentCoordinator::broadcast_message(const std::string& from_agent,
                                          const std::vector<double>& message)
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    for (auto& [id, agent] : agents_) {
        if (id != from_agent) {
            agent->receive_agent_input(from_agent, message);
        }
    }
}

size_t AgentCoordinator::get_agent_count() const
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    return agents_.size();
}

std::shared_ptr<CognitiveAgent> AgentCoordinator::get_agent(
    const std::string& agent_id) const
{
    std::lock_guard<std::mutex> lock(coordinator_mutex_);
    auto it = agents_.find(agent_id);
    if (it != agents_.end()) return it->second;
    return nullptr;
}

} // namespace opencog
