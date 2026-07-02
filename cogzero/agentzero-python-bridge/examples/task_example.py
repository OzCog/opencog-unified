#!/usr/bin/env python3
"""
Task Management Example

Demonstrates goal decomposition and task execution.
"""

from opencog.atomspace import AtomSpace, ConceptNode
from opencog.agentzero import TaskManager, AgentZero


def main():
    """Run task management example."""
    print("=" * 60)
    print("Agent-Zero - Task Management Example")
    print("=" * 60)
    
    # Create AtomSpace and task manager
    print("\n1. Creating task manager...")
    atomspace = AtomSpace()
    tm = TaskManager(atomspace)
    print(f"   Task manager: {tm}")
    
    # Create a hierarchical goal structure
    print("\n2. Creating hierarchical goals...")
    main_goal = ConceptNode("BuildWebApp")
    print(f"   Main goal: {main_goal}")
    
    # Decompose into subgoals
    subgoals = [
        ConceptNode("DesignUI"),
        ConceptNode("ImplementBackend"),
        ConceptNode("SetupDatabase"),
        ConceptNode("WriteDocs")
    ]
    
    print("\n3. Decomposing goal into tasks...")
    success = tm.decompose_goal(main_goal, subgoals)
    print(f"   Decomposition: {'✓' if success else '✗'}")
    for sg in subgoals:
        print(f"   - {sg}")
    
    # Check pending tasks
    print("\n4. Checking task status...")
    pending = tm.get_pending_tasks()
    completed = tm.get_completed_tasks()
    print(f"   Pending tasks: {len(pending)}")
    print(f"   Completed tasks: {len(completed)}")
    
    # Execute tasks
    print("\n5. Executing tasks...")
    for i in range(3):
        success = tm.execute_next_task()
        print(f"   Task {i+1}: {'✓ Executed' if success else '✗ No tasks'}")
        print(f"   Pending: {tm.pending_count}, Completed: {tm.completed_count}")
    
    # Check goal achievement
    print("\n6. Checking goal achievement...")
    achieved = tm.is_goal_achieved(main_goal)
    print(f"   Main goal achieved: {'Yes' if achieved else 'Not yet'}")
    
    print("\n" + "=" * 60)
    print("Task management example completed!")
    print("=" * 60)


def advanced_example():
    """Run advanced example using full AgentZero API."""
    print("\n\n" + "=" * 60)
    print("Advanced Task Management with AgentZero")
    print("=" * 60)
    
    with AgentZero() as agent:
        print("\n1. Adding goals through AgentZero...")
        agent.add_goal("LearnMachineLearning", priority=0.9)
        agent.add_goal("BuildNeuralNetwork", priority=0.8)
        
        print(f"\n2. Active goals: {len(agent.goals)}")
        print(f"   Pending tasks: {len(agent.pending_tasks)}")
        
        print("\n3. Running agent for 5 cycles...")
        agent.run(cycles=5)
        
        print(f"\n4. Final statistics:")
        for key, value in agent.statistics.items():
            print(f"   {key}: {value}")


if __name__ == '__main__':
    main()
    advanced_example()
