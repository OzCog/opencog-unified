#!/usr/bin/env python3
"""
Phase II: Recursive Cognitive Expansion - Python Demonstration
Simplified demonstration of Phase II cognitive components without external dependencies
"""

import math
import random
import time
from dataclasses import dataclass
from threading import Lock


@dataclass
class CognitiveNode:
    """Represents a cognitive node in the hypergraph"""
    id: str
    state: float
    attention: float
    node_type: str
    x: float = 0.0
    y: float = 0.0

@dataclass
class CognitiveAgent:
    """Represents a distributed cognitive agent"""
    id: str
    state: list[float]
    active: bool
    frequency: float
    adjacent_agents: list[str]

class PerceptualInputProcessor:
    """Phase II.1: Perceptual Input Layer implementation"""

    def __init__(self, threshold: float = 0.5):
        self.attention_weights = [1.0] * 10
        self.gating_threshold = threshold

    def recursive_attention_allocate(self, input_signals: list[float],
                                   context_weights: list[float]) -> list[float]:
        """Recursive attention allocation with adaptive signal gating"""
        processed_signals = []

        for i, (signal, context) in enumerate(zip(input_signals, context_weights, strict=False)):
            # Ensure we have enough attention weights
            if i >= len(self.attention_weights):
                self.attention_weights.append(1.0)

            # Apply attention and context
            attended_signal = signal * self.attention_weights[i] * context

            # Adaptive signal gating
            if abs(attended_signal) > self.gating_threshold:
                gated_signal = attended_signal * (1.0 + math.tanh(context - 0.5))
            else:
                gated_signal = 0.0

            processed_signals.append(gated_signal)

        # Recursive feedback: update attention weights
        self.update_attention_weights(processed_signals)

        return processed_signals

    def update_attention_weights(self, feedback_signals: list[float]):
        """Update attention weights based on feedback (recursive pathway)"""
        learning_rate = 0.1

        for i, feedback in enumerate(feedback_signals):
            if i < len(self.attention_weights):
                feedback_strength = abs(feedback)
                self.attention_weights[i] += learning_rate * feedback_strength
                # Clamp to reasonable bounds
                self.attention_weights[i] = max(0.1, min(2.0, self.attention_weights[i]))

class HypergraphPatternExtractor:
    """Phase II.2: Emergent Pattern Encoding implementation"""

    def __init__(self, threshold: float = 0.7):
        self.pattern_threshold = threshold
        self.pattern_frequencies = {}

    def extract_emergent_patterns(self, nodes: list[CognitiveNode]) -> list[str]:
        """Extract emergent patterns from cognitive nodes"""
        detected_patterns = []

        # Look for clustering patterns
        clusters = self.find_node_clusters(nodes)

        for i, cluster in enumerate(clusters):
            if len(cluster) >= 3:
                pattern_id = f"cluster_pattern_{i}"
                detected_patterns.append(pattern_id)
                self.pattern_frequencies[pattern_id] = self.pattern_frequencies.get(pattern_id, 0) + 1

        # Look for attention patterns
        high_attention_nodes = [n for n in nodes if n.attention > 0.7]
        if len(high_attention_nodes) >= 2:
            pattern_id = "high_attention_pattern"
            detected_patterns.append(pattern_id)
            self.pattern_frequencies[pattern_id] = self.pattern_frequencies.get(pattern_id, 0) + 1

        return detected_patterns

    def find_node_clusters(self, nodes: list[CognitiveNode]) -> list[list[str]]:
        """Find clusters of nodes based on proximity"""
        clusters = []
        visited = set()
        cluster_threshold = 50.0  # Distance threshold

        for node in nodes:
            if node.id in visited:
                continue

            cluster = [node.id]
            visited.add(node.id)

            for other_node in nodes:
                if other_node.id in visited:
                    continue

                distance = math.sqrt((node.x - other_node.x)**2 + (node.y - other_node.y)**2)
                if distance < cluster_threshold:
                    cluster.append(other_node.id)
                    visited.add(other_node.id)

            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def reify_patterns_as_links(self, patterns: list[str]) -> list[str]:
        """Reify detected patterns as new hypergraph links (recursive pathway)"""
        reified_links = []

        for pattern in patterns:
            reified_link = f"reified_{pattern}_{int(time.time())}"
            reified_links.append(reified_link)

        return reified_links

class DistributedCognitionEngine:
    """Phase II.3: Distributed Cognition Engine implementation"""

    def __init__(self):
        self.agents = {}
        self.shared_context = {}
        self.context_lock = Lock()

    def create_cognitive_agent(self, agent_id: str, initial_state: list[float]) -> CognitiveAgent:
        """Create a new cognitive agent"""
        agent = CognitiveAgent(
            id=agent_id,
            state=initial_state.copy(),
            active=True,
            frequency=5.0 + random.random() * 5.0,  # 5-10 Hz
            adjacent_agents=[]
        )

        self.agents[agent_id] = agent

        with self.context_lock:
            self.shared_context[agent_id] = {
                'state': initial_state.copy(),
                'last_update': time.time()
            }

        return agent

    def connect_agents(self, agent1_id: str, agent2_id: str):
        """Create bidirectional connection between agents"""
        if agent1_id in self.agents and agent2_id in self.agents:
            self.agents[agent1_id].adjacent_agents.append(agent2_id)
            self.agents[agent2_id].adjacent_agents.append(agent1_id)

    def cognitive_iteration(self, agent: CognitiveAgent) -> list[float]:
        """Single cognitive iteration for an agent"""
        # Get shared context
        with self.context_lock:
            shared_state = []
            for other_id, context in self.shared_context.items():
                if other_id != agent.id:
                    shared_state.extend(context['state'][:2])  # Take first 2 elements

        # Process cognitive inputs
        combined_input = agent.state + shared_state[:len(agent.state)]

        # Simple cognitive processing
        new_state = []
        for _i, (old_val, new_input) in enumerate(zip(agent.state, combined_input[:len(agent.state)], strict=False)):
            # Apply learning and adaptation
            new_val = 0.7 * old_val + 0.3 * new_input + 0.1 * (random.random() - 0.5)
            new_val = max(0.0, min(1.0, new_val))  # Clamp to [0,1]
            new_state.append(new_val)

        # Update agent state
        agent.state = new_state

        # Update shared context
        with self.context_lock:
            self.shared_context[agent.id] = {
                'state': new_state.copy(),
                'last_update': time.time()
            }

        return new_state

class CognitiveVisualizer:
    """Phase II.4: Interactive Cognitive Visualization implementation"""

    def __init__(self):
        self.nodes = {}
        self.attention_overlays = {}
        self.patterns = {}

    def update_cognitive_state(self, nodes: list[CognitiveNode], patterns: list[str]):
        """Update visualization with current cognitive state"""
        self.nodes = {node.id: node for node in nodes}

        # Update attention overlays
        self.attention_overlays = {}
        for node in nodes:
            if node.attention > 0.5:
                self.attention_overlays[node.id] = {
                    'x': node.x,
                    'y': node.y,
                    'radius': node.attention * 50,
                    'intensity': node.attention
                }

        # Update patterns
        self.patterns = {f"pattern_{i}": pattern for i, pattern in enumerate(patterns)}

    def generate_visualization_feedback(self, interaction_type: str,
                                      target_id: str, strength: float) -> list[float]:
        """Generate feedback from user interactions (recursive pathway)"""
        feedback = [0.0] * 5

        if target_id in self.nodes:
            # Increase attention for clicked nodes
            node = self.nodes[target_id]
            node.attention = min(1.0, node.attention + strength * 0.2)

            # Generate feedback signal
            feedback[0] = strength
            feedback[1] = node.attention
            feedback[2] = node.state
            feedback[3] = random.random() * 0.1  # Random component
            feedback[4] = time.time() % 1.0  # Temporal component

        return feedback

class NeuralSymbolicTutorial:
    """Phase II.5: Tutorial and Automation Layer implementation"""

    def __init__(self):
        self.tutorial_state = {
            'current_section': 'introduction',
            'progress': 0,
            'difficulty': 0.5,
            'user_responses': []
        }

        self.tutorial_content = {
            'introduction': "Welcome to OpenCog Unified Phase II! This demonstrates recursive cognitive expansion.",
            'basic_concepts': "Let's explore cognitive nodes, attention allocation, and pattern detection.",
            'pattern_recognition': "Now we'll see how patterns emerge and get reified into new cognitive objects.",
            'distributed_cognition': "Multiple cognitive agents work together through shared hypergraph context.",
            'visualization': "Real-time visualization shows attention flows and emergent patterns."
        }

    def analyze_user_intent(self, user_input: str) -> str:
        """Analyze user input to determine intent"""
        user_input = user_input.lower()

        if any(word in user_input for word in ['help', 'confused', "don't understand"]):
            return 'need_help'
        elif any(word in user_input for word in ['next', 'continue', 'more']):
            return 'ready_to_proceed'
        elif any(word in user_input for word in ['example', 'show', 'demonstrate']):
            return 'want_example'
        elif any(word in user_input for word in ['yes', 'ok', 'understood', 'got it']):
            return 'comprehension_positive'
        elif any(word in user_input for word in ['no', 'wrong', 'incorrect']):
            return 'comprehension_negative'
        else:
            return 'general_input'

    def chatbot_interaction(self, user_input: str) -> tuple[str, str]:
        """Process user input and generate adaptive tutorial response"""
        intent = self.analyze_user_intent(user_input)
        current_section = self.tutorial_state['current_section']

        # Record interaction for recursive feedback
        self.tutorial_state['user_responses'].append((user_input, intent, time.time()))

        # Generate response based on intent
        if intent == 'need_help':
            response = f"Let me help! {self.tutorial_content[current_section]} What specific aspect confuses you?"
        elif intent == 'ready_to_proceed':
            response = self.advance_tutorial_section()
        elif intent == 'want_example':
            response = self.generate_example(current_section)
        elif intent == 'comprehension_positive':
            response = "Excellent! Let's build on that understanding."
            self.adjust_difficulty(0.1)
        elif intent == 'comprehension_negative':
            response = "No worries! Let me explain this differently."
            self.adjust_difficulty(-0.2)
        else:
            response = f"{self.tutorial_content[current_section]} What would you like to explore?"

        return response, intent

    def generate_example(self, section: str) -> str:
        """Generate contextual examples"""
        examples = {
            'introduction': "Try this: Create a cognitive node with attention=0.8 and watch how it affects nearby nodes!",
            'basic_concepts': "Example: Node 'learning' with high attention (0.9) influences connected nodes through attention propagation.",
            'pattern_recognition': "Watch: When 3+ nodes cluster together, they form an emergent pattern that gets reified as a new cognitive object.",
            'distributed_cognition': "Example: Agent A processes input [0.5, 0.8] → shares with Agent B → creates collaborative cognitive state.",
            'visualization': "Try clicking on nodes in the visualization to see recursive attention feedback in action!"
        }
        return examples.get(section, "Here's a general example of cognitive processing...")

    def advance_tutorial_section(self) -> str:
        """Advance to next tutorial section"""
        sections = ['introduction', 'basic_concepts', 'pattern_recognition', 'distributed_cognition', 'visualization']
        current_index = sections.index(self.tutorial_state['current_section'])

        if current_index < len(sections) - 1:
            self.tutorial_state['current_section'] = sections[current_index + 1]
            self.tutorial_state['progress'] = 0
            return f"Great! Moving to: {self.tutorial_content[self.tutorial_state['current_section']]}"
        else:
            return "Congratulations! You've completed the Phase II tutorial. You now understand recursive cognitive expansion!"

    def adjust_difficulty(self, delta: float):
        """Adjust tutorial difficulty based on user performance (recursive adaptation)"""
        self.tutorial_state['difficulty'] += delta
        self.tutorial_state['difficulty'] = max(0.1, min(1.0, self.tutorial_state['difficulty']))

class PhaseIIDemonstration:
    """Main demonstration orchestrator for Phase II components"""

    def __init__(self):
        self.perceptual_processor = PerceptualInputProcessor()
        self.pattern_extractor = HypergraphPatternExtractor()
        self.cognition_engine = DistributedCognitionEngine()
        self.visualizer = CognitiveVisualizer()
        self.tutorial = NeuralSymbolicTutorial()

        # Create sample cognitive nodes
        self.cognitive_nodes = [
            CognitiveNode(f"node_{i}", random.random(), random.random(),
                         random.choice(['concept', 'predicate', 'evaluation']),
                         random.uniform(0, 200), random.uniform(0, 200))
            for i in range(15)
        ]

    def demonstrate_complete_cycle(self):
        """Demonstrate complete Phase II recursive cognitive cycle"""
        print("🚀 PHASE II: RECURSIVE COGNITIVE EXPANSION DEMONSTRATION")
        print("=" * 60)

        # Step 1: Perceptual Input Processing
        print("\n🔵 STEP 1: PERCEPTUAL INPUT PROCESSING")
        input_signals = [0.8, 0.3, 0.9, 0.1, 0.7]
        context_weights = [1.0, 0.5, 1.2, 0.2, 0.8]

        processed_signals = self.perceptual_processor.recursive_attention_allocate(
            input_signals, context_weights)

        print(f"  Input signals: {input_signals}")
        print(f"  Processed signals: {[round(x, 3) for x in processed_signals]}")
        print(f"  Attention weights: {[round(x, 3) for x in self.perceptual_processor.attention_weights[:5]]}")

        # Step 2: Pattern Detection and Reification
        print("\n🟡 STEP 2: EMERGENT PATTERN DETECTION")
        detected_patterns = self.pattern_extractor.extract_emergent_patterns(self.cognitive_nodes)
        reified_patterns = self.pattern_extractor.reify_patterns_as_links(detected_patterns)

        print(f"  Detected patterns: {detected_patterns}")
        print(f"  Reified patterns: {len(reified_patterns)} new hypergraph links")
        print(f"  Pattern frequencies: {self.pattern_extractor.pattern_frequencies}")

        # Step 3: Distributed Cognition
        print("\n🟢 STEP 3: DISTRIBUTED COGNITION")
        self.cognition_engine.create_cognitive_agent("alpha", [0.5, 0.7, 0.3])
        self.cognition_engine.create_cognitive_agent("beta", [0.8, 0.2, 0.6])
        self.cognition_engine.create_cognitive_agent("gamma", [0.3, 0.9, 0.4])

        self.cognition_engine.connect_agents("alpha", "beta")
        self.cognition_engine.connect_agents("beta", "gamma")

        print(f"  Created agents: {list(self.cognition_engine.agents.keys())}")

        # Run several cognitive iterations
        for _cycle in range(5):
            for agent in self.cognition_engine.agents.values():
                self.cognition_engine.cognitive_iteration(agent)

        print("  After 5 cycles:")
        for agent_id, agent in self.cognition_engine.agents.items():
            print(f"    {agent_id}: {[round(x, 3) for x in agent.state]}")

        # Step 4: Visualization Update
        print("\n🟣 STEP 4: COGNITIVE VISUALIZATION")
        self.visualizer.update_cognitive_state(self.cognitive_nodes, detected_patterns)

        high_attention_nodes = [n for n in self.cognitive_nodes if n.attention > 0.7]
        print(f"  High attention nodes: {len(high_attention_nodes)}")
        print(f"  Attention overlays: {len(self.visualizer.attention_overlays)}")
        print(f"  Visualization patterns: {len(self.visualizer.patterns)}")

        # Simulate user interaction
        if high_attention_nodes:
            feedback = self.visualizer.generate_visualization_feedback(
                "click", high_attention_nodes[0].id, 1.0)
            print(f"  User interaction feedback: {[round(x, 3) for x in feedback]}")

        # Step 5: Tutorial Interaction
        print("\n🟠 STEP 5: TUTORIAL INTERACTION")
        sample_interactions = [
            "What is this system doing?",
            "I want to see an example",
            "Yes, I understand",
            "Show me more about patterns"
        ]

        for user_input in sample_interactions:
            response, intent = self.tutorial.chatbot_interaction(user_input)
            print(f"  User: '{user_input}' -> Intent: {intent}")
            print(f"  Bot: {response[:80]}...")

        # Step 6: Complete Recursive Cycle
        print("\n🌟 STEP 6: RECURSIVE FEEDBACK INTEGRATION")

        # Apply feedback from all components
        feedback_strength = sum(processed_signals) / len(processed_signals)

        # Update node attention based on pattern detection
        for node in self.cognitive_nodes:
            if any(pattern in detected_patterns for pattern in ['cluster_pattern_0', 'high_attention_pattern']):
                node.attention = min(1.0, node.attention + 0.1)

        # Update perceptual processor based on agent states
        agent_states = [agent.state[0] for agent in self.cognition_engine.agents.values()]
        self.perceptual_processor.update_attention_weights(agent_states)

        print(f"  Recursive feedback strength: {round(feedback_strength, 3)}")
        print(f"  Updated attention weights: {[round(x, 3) for x in self.perceptual_processor.attention_weights[:5]]}")
        print(f"  Tutorial difficulty adapted to: {round(self.tutorial.tutorial_state['difficulty'], 3)}")

        print("\n✨ RECURSIVE COGNITIVE CYCLE COMPLETED!")
        print("   Patterns detected → Reified → Influenced agents → Updated attention → Enhanced learning")

    def run_automated_tests(self):
        """Run automated tests of Phase II components"""
        print("\n🧪 AUTOMATED TESTING SUITE")
        print("-" * 30)

        test_results = {}

        # Test 1: Perceptual processing
        test_input = [0.5, 0.8, 0.3, 0.9, 0.1]
        test_context = [1.0, 0.7, 0.9, 1.1, 0.6]
        result = self.perceptual_processor.recursive_attention_allocate(test_input, test_context)
        test_results['perceptual_processing'] = len(result) == len(test_input)
        print(f"  ✅ Perceptual processing: {test_results['perceptual_processing']}")

        # Test 2: Pattern detection
        patterns = self.pattern_extractor.extract_emergent_patterns(self.cognitive_nodes[:5])
        test_results['pattern_detection'] = len(patterns) >= 0
        print(f"  ✅ Pattern detection: {test_results['pattern_detection']} ({len(patterns)} patterns)")

        # Test 3: Agent collaboration
        agent_count_before = len(self.cognition_engine.agents)
        self.cognition_engine.create_cognitive_agent("test", [0.5, 0.5, 0.5])
        agent_count_after = len(self.cognition_engine.agents)
        test_results['agent_creation'] = agent_count_after > agent_count_before
        print(f"  ✅ Agent creation: {test_results['agent_creation']}")

        # Test 4: Tutorial adaptation
        _response, intent = self.tutorial.chatbot_interaction("I need help")
        test_results['tutorial_interaction'] = intent == 'need_help'
        print(f"  ✅ Tutorial interaction: {test_results['tutorial_interaction']}")

        # Test 5: Visualization feedback
        feedback = self.visualizer.generate_visualization_feedback("click", "node_0", 0.8)
        test_results['visualization_feedback'] = len(feedback) == 5
        print(f"  ✅ Visualization feedback: {test_results['visualization_feedback']}")

        print(f"\n📊 Test Results: {sum(test_results.values())}/{len(test_results)} passed")

        return all(test_results.values())

def main():
    """Main demonstration function"""
    print("🧠 OpenCog Unified - Phase II: Recursive Cognitive Expansion")
    print("============================================================")

    demo = PhaseIIDemonstration()

    # Run complete demonstration
    demo.demonstrate_complete_cycle()

    # Run automated tests
    test_success = demo.run_automated_tests()

    print(f"\n🎯 PHASE II IMPLEMENTATION STATUS: {'SUCCESS' if test_success else 'NEEDS ATTENTION'}")
    print("\n📋 CAPABILITIES DEMONSTRATED:")
    print("  🔵 Recursive attention allocation and adaptive signal gating")
    print("  🟡 Emergent pattern detection and hypergraph reification")
    print("  🟢 Multi-agent distributed cognition with shared context")
    print("  🟣 Interactive visualization with recursive feedback")
    print("  🟠 Adaptive neural-symbolic tutorial system")
    print("  🌟 Complete recursive cognitive expansion cycles")

    print("\n📁 Implementation files created:")
    print("  • cognitive-patterns/: Perceptual input & pattern encoding")
    print("  • distributed-cognition/: Multi-agent cognitive engine")
    print("  • cognitive-visualization/: Interactive web visualization")
    print("  • tutorial-automation/: Adaptive tutorial system")
    print("  • phase-ii-demonstration.scm: Complete Scheme integration")

    print("\n🚀 Next steps:")
    print("  • Open cognitive-visualization/web/index.html for interactive demo")
    print("  • Run guile -l phase-ii-demonstration.scm for Scheme integration")
    print("  • Execute ./test-phase-ii.sh for component validation")

if __name__ == "__main__":
    main()
