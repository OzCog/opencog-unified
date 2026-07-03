/*
 * CognitiveAgent.h
 * 
 * Phase II.3: Distributed Cognition Engine
 * Multi-agent Scheme modules for parallel cognitive cycles
 */

#ifndef _OPENCOG_COGNITIVE_AGENT_H
#define _OPENCOG_COGNITIVE_AGENT_H

#include <memory>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <atomic>

namespace opencog {

/**
 * Cognitive Agent
 * 
 * Individual agent in the distributed cognition system.
 * Recursive implementation: Agent output becomes dynamic input for adjacent agents.
 */
class CognitiveAgent
{
private:
    // Agent identifier
    std::string agent_id_;
    
    // Agent state and cognitive cycle
    std::vector<double> internal_state_;
    std::atomic<bool> active_;
    std::atomic<bool> processing_;
    
    // Thread management
    std::unique_ptr<std::thread> cognitive_thread_;
    std::mutex state_mutex_;
    std::mutex cycle_mutex_;  // Separate mutex for cycle sleep (avoids blocking coordination)
    std::condition_variable cycle_cv_;
    
    // Cognitive cycle parameters
    double cycle_frequency_;  // Hz
    int max_cycle_iterations_;
    
    // Inter-agent communication
    std::vector<std::string> adjacent_agents_;
    std::vector<double> input_from_agents_;
    std::vector<double> output_to_agents_;

public:
    CognitiveAgent(const std::string& id, double frequency = 10.0, int max_iterations = 1000);
    ~CognitiveAgent();

    /**
     * Start the cognitive agent's processing cycle
     */
    void start_cognitive_cycle();

    /**
     * Stop the cognitive agent
     */
    void stop_cognitive_cycle();

    /**
     * Single cognitive processing iteration
     * Recursive pathway: processes inputs, updates state, generates outputs
     * 
     * @param shared_context Shared hypergraph context from other agents
     * @return Output vector for distribution to adjacent agents
     */
    std::vector<double> cognitive_iteration(
        const std::vector<double>& shared_context);

    /**
     * Receive input from adjacent agents
     * Recursive implementation: agent output becomes input for others
     * 
     * @param agent_id Source agent identifier
     * @param input_data Data received from the agent
     */
    void receive_agent_input(const std::string& agent_id, 
                           const std::vector<double>& input_data);

    /**
     * Add connection to adjacent agent
     * Creates bidirectional communication channel
     * 
     * @param agent_id Identifier of agent to connect to
     */
    void add_adjacent_agent(const std::string& agent_id);

    /**
     * Update internal cognitive state
     * 
     * @param state_updates Vector of state modifications
     */
    void update_internal_state(const std::vector<double>& state_updates);

    /**
     * Get current cognitive state (thread-safe)
     */
    std::vector<double> get_cognitive_state() const;

    /**
     * Get last computed cognitive output (for inter-agent routing)
     * This is the processed output, not the raw internal state.
     */
    std::vector<double> get_cognitive_output() const;

    /**
     * Set cognitive cycle frequency
     */
    void set_cycle_frequency(double frequency) { cycle_frequency_ = frequency; }

    /**
     * Get agent identifier
     */
    std::string get_agent_id() const { return agent_id_; }

    /**
     * Check if agent is currently active
     */
    bool is_active() const { return active_.load(); }

    /**
     * Get list of adjacent agents
     */
    std::vector<std::string> get_adjacent_agents() const { return adjacent_agents_; }

private:
    /**
     * Main cognitive processing loop (runs in separate thread)
     */
    void cognitive_processing_loop();

    /**
     * Process perceptual inputs and generate cognitive response
     * 
     * @param inputs Combined inputs from environment and other agents
     * @return Processed cognitive output
     */
    std::vector<double> process_cognitive_inputs(const std::vector<double>& inputs);

    /**
     * Apply learning and adaptation to internal state
     * 
     * @param feedback Feedback from cognitive processing results
     */
    void apply_cognitive_learning(const std::vector<double>& feedback);
};

} // namespace opencog

#endif // _OPENCOG_COGNITIVE_AGENT_H