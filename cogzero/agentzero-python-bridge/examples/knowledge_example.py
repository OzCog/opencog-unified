#!/usr/bin/env python3
"""
Knowledge Integration Example

Demonstrates knowledge operations using the Python bridge.
"""

from opencog.atomspace import AtomSpace, ConceptNode, InheritanceLink
from opencog.agentzero import KnowledgeIntegrator


def main():
    """Run knowledge integration example."""
    print("=" * 60)
    print("Agent-Zero - Knowledge Integration Example")
    print("=" * 60)
    
    # Create AtomSpace and integrator
    print("\n1. Creating knowledge base...")
    atomspace = AtomSpace()
    ki = KnowledgeIntegrator(atomspace)
    print(f"   Knowledge integrator: {ki}")
    
    # Add some knowledge
    print("\n2. Adding knowledge to AtomSpace...")
    animal = ConceptNode("Animal")
    mammal = ConceptNode("Mammal")
    dog = ConceptNode("Dog")
    cat = ConceptNode("Cat")
    
    # Create inheritance hierarchy
    ki.add_knowledge(InheritanceLink(mammal, animal))
    ki.add_knowledge(InheritanceLink(dog, mammal))
    ki.add_knowledge(InheritanceLink(cat, mammal))
    print("   Added: Mammal → Animal")
    print("   Added: Dog → Mammal")
    print("   Added: Cat → Mammal")
    
    # Set truth values
    print("\n3. Setting truth values...")
    ki.set_truth_value(dog, 0.95, 0.9)
    ki.set_truth_value(cat, 0.98, 0.95)
    print(f"   Dog truth value: {ki.get_truth_value(dog):.2f}")
    print(f"   Cat truth value: {ki.get_truth_value(cat):.2f}")
    
    # Query knowledge
    print("\n4. Querying knowledge...")
    mammal_subclasses = ki.query_subclasses(mammal)
    print(f"   Subclasses of Mammal: {mammal_subclasses}")
    
    animal_subclasses = ki.query_subclasses(animal)
    print(f"   Subclasses of Animal: {animal_subclasses}")
    
    # Query instances
    print("\n5. Querying instances...")
    mammal_instances = ki.query_instances(mammal)
    print(f"   Instances of Mammal: {mammal_instances}")
    
    print("\n" + "=" * 60)
    print("Knowledge integration example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
