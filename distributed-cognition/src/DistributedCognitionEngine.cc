/*
 * DistributedCognitionEngine.cc
 *
 * Top-level engine for distributed cognition dynamics.
 */

#include "DistributedCognitionEngine.h"
#include <chrono>

namespace opencog {

DistributedCognitionEngine::DistributedCognitionEngine(const EngineConfig& config)
    : config_(config),
      engine_running_(false)
{
    metrics_ = {};
    metrics_.total_cycles = 0;
    metrics_.total_messages_routed = 0;
    metrics_.avg_cycle_duration_ms = 0.0;
    metrics_.total_attention_allocated = 0.0;
    metrics_.system_entropy = 0.0;
}

DistributedCognitionEngine::~DistributedCognitionEngine()
{
    stop();
}

bool DistributedCognitionEngine::initialize()
{
    shared_context_ = std::make_shared<SharedHypergraphContext>();
    coordinator_ = std::make_unique<AgentCoordinator>(
        config_.max_agents, config_.coordination_interval_ms);

    // Initialize ECAN resource manager with default config
    ECANResourceManager::ResourceConfig ecan_config;
    ecan_config.total_sti_budget = 1000.0;
    ecan_config.rent_rate = 0.01;
    ecan_config.wage_rate = 0.05;
    ecan_config.tax_rate = 0.02;
    resource_manager_ = std::make_unique<ECANResourceManager>(ecan_config);

    return true;
}

bool DistributedCognitionEngine::start()
{
    if (!coordinator_ || !resource_manager_) {
        if (!initialize()) return false;
    }

    engine_running_.store(true);
    metrics_.start_time = std::chrono::steady_clock::now();
    coordinator_->start_all_agents();
    return true;
}

void DistributedCognitionEngine::stop()
{
    engine_running_.store(false);
    if (coordinator_) {
        coordinator_->stop_all_agents();
    }
}

void DistributedCognitionEngine::engine_cycle()
{
    if (!engine_running_.load()) return;

    auto cycle_start = std::chrono::steady_clock::now();

    // Step 1: Run ECAN resource allocation cycle
    if (resource_manager_) {
        resource_manager_->allocation_cycle();
    }

    // Step 2: Run agent coordination cycle
    if (coordinator_) {
        coordinator_->coordination_cycle();
    }

    // Step 3: Synchronize shared context
    if (shared_context_ && coordinator_) {
        auto all_states = coordinator_->get_shared_context()->get_all_agent_states();
        shared_context_->synchronize_context(all_states);
    }

    auto cycle_end = std::chrono::steady_clock::now();
    double duration_ms = std::chrono::duration<double, std::milli>(
        cycle_end - cycle_start).count();

    update_metrics(duration_ms);
}

std::string DistributedCognitionEngine::spawn_agent(
    const std::string& agent_id, double cycle_frequency)
{
    auto agent = std::make_shared<CognitiveAgent>(agent_id, cycle_frequency);

    if (coordinator_ && coordinator_->register_agent(agent)) {
        // Register with resource manager
        if (resource_manager_) {
            resource_manager_->register_agent(agent_id);
        }
        // NOTE: Do NOT start the agent's own background loop here.
        // The engine drives agents via coordination_cycle -> cognitive_iteration.
        // Starting the agent's own loop would cause dual-execution (once from
        // the agent's thread, once from the engine's coordination_cycle).
        return agent_id;
    }
    return "";
}

bool DistributedCognitionEngine::remove_agent(const std::string& agent_id)
{
    if (!coordinator_) return false;
    bool removed = coordinator_->unregister_agent(agent_id);
    if (removed && resource_manager_) {
        resource_manager_->unregister_agent(agent_id);
    }
    return removed;
}

DistributedCognitionEngine::EngineMetrics
DistributedCognitionEngine::get_metrics() const
{
    std::lock_guard<std::mutex> lock(metrics_mutex_);
    return metrics_;
}

void DistributedCognitionEngine::update_metrics(double cycle_duration_ms)
{
    std::lock_guard<std::mutex> lock(metrics_mutex_);
    metrics_.total_cycles++;

    // Exponential moving average for cycle duration
    double alpha = 0.1;
    metrics_.avg_cycle_duration_ms =
        metrics_.avg_cycle_duration_ms * (1.0 - alpha) + cycle_duration_ms * alpha;

    // Update attention allocated
    if (resource_manager_) {
        auto stats = resource_manager_->get_allocation_stats();
        metrics_.total_attention_allocated = stats.total_allocated;
        metrics_.system_entropy = stats.allocation_entropy;
    }
}

} // namespace opencog
