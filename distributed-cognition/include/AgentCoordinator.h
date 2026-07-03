/*
 * AgentCoordinator.h
 *
 * Phase II.3: Agent coordination for distributed cognitive processing.
 * Manages lifecycle and communication between CognitiveAgent instances.
 */

#ifndef _OPENCOG_AGENT_COORDINATOR_H
#define _OPENCOG_AGENT_COORDINATOR_H

#include <memory>
#include <vector>
#include <map>
#include <string>
#include <mutex>
#include <atomic>

#include "CognitiveAgent.h"
#include "SharedHypergraphContext.h"

namespace opencog {

/**
 * Agent Coordinator
 *
 * Orchestrates the lifecycle and communication between multiple
 * CognitiveAgent instances in a distributed cognition system.
 * Manages agent registration, message routing, and collective
 * cognitive cycle synchronization.
 */
class AgentCoordinator
{
private:
    std::map<std::string, std::shared_ptr<CognitiveAgent>> agents_;
    std::shared_ptr<SharedHypergraphContext> shared_context_;
    mutable std::mutex coordinator_mutex_;
    std::atomic<bool> running_;
    std::atomic<uint64_t> cycle_count_;

    // Coordination parameters
    double sync_interval_ms_;
    size_t max_agents_;

public:
    AgentCoordinator(size_t max_agents = 64, double sync_interval_ms = 100.0);
    ~AgentCoordinator();

    /**
     * Register a cognitive agent with the coordinator
     */
    bool register_agent(std::shared_ptr<CognitiveAgent> agent);

    /**
     * Remove an agent from coordination
     */
    bool unregister_agent(const std::string& agent_id);

    /**
     * Start coordinated cognitive processing for all agents
     */
    void start_all_agents();

    /**
     * Stop all coordinated agents
     */
    void stop_all_agents();

    /**
     * Perform one coordination cycle:
     * gather agent states, update shared context, distribute context
     */
    void coordination_cycle();

    /**
     * Route message between agents
     */
    void route_message(const std::string& from_agent,
                       const std::string& to_agent,
                       const std::vector<double>& message);

    /**
     * Broadcast message to all agents
     */
    void broadcast_message(const std::string& from_agent,
                           const std::vector<double>& message);

    /**
     * Get the shared hypergraph context
     */
    std::shared_ptr<SharedHypergraphContext> get_shared_context() const {
        return shared_context_;
    }

    /**
     * Get number of registered agents
     */
    size_t get_agent_count() const;

    /**
     * Get total coordination cycles completed
     */
    uint64_t get_cycle_count() const { return cycle_count_.load(); }

    /**
     * Check if coordinator is running
     */
    bool is_running() const { return running_.load(); }

    /**
     * Get agent by ID
     */
    std::shared_ptr<CognitiveAgent> get_agent(const std::string& agent_id) const;
};

} // namespace opencog

#endif // _OPENCOG_AGENT_COORDINATOR_H
