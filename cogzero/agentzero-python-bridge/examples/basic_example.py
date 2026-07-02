#!/usr/bin/env python3
"""
Basic Agent-Zero Example

Demonstrates basic usage of the Agent-Zero Python bridge.
"""

from opencog.atomspace import AtomSpace, ConceptNode
from opencog.agentzero import AgentZero


def main():
    """Run basic agent example."""
    print("=" * 60)
    print("Agent-Zero Python Bridge - Basic Example")
    print("=" * 60)
    
    # Create agent with default AtomSpace
    print("\n1. Creating Agent-Zero instance...")
    agent = AgentZero()
    print(f"   Agent created: {agent}")
    print(f"   Status: {agent.status}")
    
    # Add some goals
    print("\n2. Adding goals...")
    goal1 = agent.add_goal("LearnPython", priority=0.9)
    goal2 = agent.add_goal("BuildRobot", priority=0.7)
    print(f"   Added goals: {goal1}, {goal2}")
    
    # Execute some cognitive cycles
    print("\n3. Running cognitive cycles...")
    for i in range(5):
        success = agent.step()
        print(f"   Cycle {i+1}: {'✓' if success else '✗'}")
    
    # Check statistics
    print("\n4. Agent statistics:")
    stats = agent.statistics
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Shutdown
    print("\n5. Shutting down agent...")
    agent.shutdown()
    print("   Agent shutdown complete")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
