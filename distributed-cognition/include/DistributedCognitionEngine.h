/*
 * DistributedCognitionEngine.h
 *
 * Phase II.3: Top-level engine for distributed cognition dynamics.
 * Integrates AgentCoordinator, SharedHypergraphContext, ECAN resources,
 * and distributed AtomSpace sync into a unified cognitive system.
 */

#ifndef _OPENCOG_DISTRIBUTED_COGNITION_ENGINE_H
#define _OPENCOG_DISTRIBUTED_COGNITION_ENGINE_H

#include <memory>
#include <string>
#include <vector>
#include <atomic>
#include <chrono>

#include "AgentCoordinator.h"
#include "ECANResourceManager.h"
#include "DistributedAtomSpaceSync.h"
#include "SharedHypergraphContext.h"

namespace opencog {

/**
 * Distributed Cognition Engine
 *
 * Top-level orchestrator that brings together multi-agent coordination,
 * ECAN resource management, and distributed synchronization to form
 * a coherent distributed cognition system with emergent dynamics.
 */
class DistributedCognitionEngine
{
public:
    struct EngineConfig {
        size_t max_agents = 64;
        double coordination_interval_ms = 100.0;
        double ecan_cycle_period_ms = 50.0;
        bool enable_distributed_sync = true;
        bool enable_oscillation_monitoring = false;
    };

    struct EngineMetrics {
        uint64_t total_cycles;
        uint64_t total_messages_routed;
        double avg_cycle_duration_ms;
        double total_attention_allocated;
        double system_entropy;
        std::chrono::steady_clock::time_point start_time;
    };

private:
    EngineConfig config_;
    std::unique_ptr<AgentCoordinator> coordinator_;
    std::unique_ptr<ECANResourceManager> resource_manager_;
    std::shared_ptr<SharedHypergraphContext> shared_context_;
    std::atomic<bool> engine_running_;
    EngineMetrics metrics_;
    mutable std::mutex metrics_mutex_;

public:
    explicit DistributedCognitionEngine(const EngineConfig& config = EngineConfig());
    ~DistributedCognitionEngine();

    /**
     * Initialize the engine with configuration
     */
    bool initialize();

    /**
     * Start the distributed cognition engine
     */
    bool start();

    /**
     * Stop the engine gracefully
     */
    void stop();

    /**
     * Execute one engine cycle (coordination + ECAN + sync)
     */
    void engine_cycle();

    /**
     * Spawn a new cognitive agent within the engine
     */
    std::string spawn_agent(const std::string& agent_id,
                           double cycle_frequency = 10.0);

    /**
     * Remove an agent from the engine
     */
    bool remove_agent(const std::string& agent_id);

    /**
     * Get current engine metrics
     */
    EngineMetrics get_metrics() const;

    /**
     * Get the coordinator for direct agent management
     */
    AgentCoordinator* get_coordinator() const { return coordinator_.get(); }

    /**
     * Get the ECAN resource manager
     */
    ECANResourceManager* get_resource_manager() const { return resource_manager_.get(); }

    /**
     * Check if engine is running
     */
    bool is_running() const { return engine_running_.load(); }

private:
    void update_metrics(double cycle_duration_ms);
};

} // namespace opencog

#endif // _OPENCOG_DISTRIBUTED_COGNITION_ENGINE_H
