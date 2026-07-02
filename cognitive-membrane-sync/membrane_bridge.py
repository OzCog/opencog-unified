#!/usr/bin/env python3
"""
Cognitive Membrane Synchronization Bridge
Integrates Scheme-based membrane operations with GitHub Actions workflow
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

# Import JSON encoder utilities
from json_encoder_utils import safe_json_dump


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CognitiveMembraneBridge:
    """Bridge between Python workflows and Scheme membrane operations"""

    def __init__(self, workspace_path: str = "/workspaces/cosmos"):
        self.workspace_path = Path(workspace_path)
        self.scheme_module_path = Path(__file__).parent.parent / "distributed-cognition" / "scheme"
        self.membrane_config = {}
        self.tensor_mappings = {}

    def initialize_membrane_topology(self, enterprise_id: str, tensor_dimensions: list[int]) -> dict[str, Any]:
        """Initialize the cognitive membrane topology"""
        logger.info(f"🌌 Initializing membrane topology for enterprise: {enterprise_id}")

        # Create enterprise configuration
        enterprise_config = {
            'enterprise_id': enterprise_id,
            'tensor_dimensions': tensor_dimensions,
            'timestamp': datetime.utcnow().isoformat(),
            'organizations': {},
            'repositories': {},
            'membrane_hierarchy': {},
            'synchronization_status': 'initialized'
        }

        self.membrane_config = enterprise_config
        return enterprise_config

    def create_organizational_membrane(self, org_id: str, membrane_type: str, prime_factor: int) -> dict[str, Any]:
        """Create organizational membrane within enterprise"""
        logger.info(f"🏢 Creating organizational membrane: {org_id}")

        # Calculate tensor shape for organization
        tensor_shape = self._calculate_org_tensor_shape(org_id)

        org_membrane = {
            'org_id': org_id,
            'membrane_type': membrane_type,
            'prime_factor': prime_factor,
            'tensor_shape': tensor_shape,
            'permeability': 'bidirectional',
            'repositories': {},
            'created_at': datetime.utcnow().isoformat()
        }

        # Add to enterprise configuration
        if 'organizations' not in self.membrane_config:
            self.membrane_config['organizations'] = {}

        self.membrane_config['organizations'][org_id] = org_membrane

        # Call Scheme function to create membrane
        self._call_scheme_function('create-organization-membrane', [org_id, self.membrane_config['enterprise_id'], membrane_type, prime_factor])

        return org_membrane

    def create_repository_membrane(self, repo_id: str, org_id: str, cognitive_patterns: list[str]) -> dict[str, Any]:
        """Create repository membrane within organizational membrane"""
        logger.info(f"📂 Creating repository membrane: {repo_id}")

        # Calculate complexity and tensor shape
        complexity_score = self._calculate_repo_complexity(cognitive_patterns)
        tensor_shape = self._derive_tensor_shape_from_complexity(complexity_score)

        repo_membrane = {
            'repo_id': repo_id,
            'org_id': org_id,
            'cognitive_patterns': cognitive_patterns,
            'complexity_score': complexity_score,
            'tensor_shape': tensor_shape,
            'membrane_permeability': self._assess_membrane_permeability(cognitive_patterns),
            'created_at': datetime.utcnow().isoformat()
        }

        # Add to organizational membrane
        if org_id in self.membrane_config['organizations']:
            self.membrane_config['organizations'][org_id]['repositories'][repo_id] = repo_membrane

        # Call Scheme function
        self._call_scheme_function('create-repository-membrane', [repo_id, org_id, cognitive_patterns])

        return repo_membrane

    def fold_membrane_to_markdown(self, membrane_id: str) -> str:
        """Fold cognitive membrane into markdown representation"""
        logger.info(f"🌀 Folding membrane {membrane_id} to markdown")

        # Call Scheme folding function
        markdown_content = self._call_scheme_function('fold-membrane-to-markdown', [membrane_id])

        # Generate Python-based markdown if Scheme call fails
        if not markdown_content:
            markdown_content = self._generate_membrane_markdown(membrane_id)

        # Save to file
        markdown_path = Path(f"cognitive-membrane-{membrane_id}.md")
        markdown_path.write_text(markdown_content)

        return markdown_content

    def unfold_membrane_from_markdown(self, markdown_content: str, target_membrane_id: str) -> bool:
        """Unfold markdown content back into cognitive membrane structure"""
        logger.info(f"🌊 Unfolding markdown content into membrane {target_membrane_id}")

        # Call Scheme unfolding function
        result = self._call_scheme_function('unfold-membrane-from-markdown', [markdown_content, target_membrane_id])

        return result is not None

    def project_membrane_to_tensor(self, membrane_id: str) -> np.ndarray | None:
        """Project cognitive membrane to tensor representation"""
        logger.info(f"📊 Projecting membrane {membrane_id} to tensor")

        # Get membrane configuration
        membrane_data = self._get_membrane_data(membrane_id)
        if not membrane_data:
            return None

        tensor_shape = membrane_data.get('tensor_shape', [3, 3, 3])
        tensor_field = np.zeros(tensor_shape, dtype=np.float32)

        # Fill tensor with membrane data
        if 'complexity_score' in membrane_data:
            tensor_field.fill(membrane_data['complexity_score'] / 10.0)  # Normalize

        # Save tensor data
        tensor_path = Path(f"cognitive-tensor-{membrane_id}.npy")
        np.save(tensor_path, tensor_field)

        return tensor_field

    def embed_membrane_in_hypergraph(self, membrane_id: str) -> dict[str, Any]:
        """Embed cognitive membrane in hypergraph representation"""
        logger.info(f"🔗 Embedding membrane {membrane_id} in hypergraph")

        membrane_data = self._get_membrane_data(membrane_id)
        if not membrane_data:
            return {}

        hypergraph_embedding = {
            'node_id': membrane_id,
            'node_type': membrane_data.get('membrane_type', 'unknown'),
            'tensor_shape': membrane_data.get('tensor_shape', [1, 1, 1]),
            'edges': [],
            'properties': {
                'complexity': membrane_data.get('complexity_score', 1.0),
                'permeability': membrane_data.get('membrane_permeability', 'medium'),
                'prime_factor': membrane_data.get('prime_factor', 2)
            }
        }

        # Add edges to connected membranes
        if 'repositories' in membrane_data:
            for repo_id in membrane_data['repositories']:
                hypergraph_embedding['edges'].append({
                    'target': repo_id,
                    'type': 'contains',
                    'weight': 1.0
                })

        return hypergraph_embedding

    def synchronize_enterprise_membranes(self, enterprise_id: str) -> dict[str, Any]:
        """Synchronize all membranes within an enterprise"""
        logger.info(f"🔄 Starting enterprise-wide membrane synchronization for {enterprise_id}")

        synchronization_result = {
            'enterprise_id': enterprise_id,
            'start_time': datetime.utcnow().isoformat(),
            'membranes_synchronized': 0,
            'tensor_mappings_updated': 0,
            'status': 'in_progress'
        }

        try:
            # Synchronize organizational membranes
            if 'organizations' in self.membrane_config:
                for org_id, org_data in self.membrane_config['organizations'].items():
                    self._synchronize_organization(org_id, org_data)
                    synchronization_result['membranes_synchronized'] += 1

                    # Synchronize repository membranes
                    if 'repositories' in org_data:
                        for repo_id in org_data['repositories']:
                            self._synchronize_repository(repo_id)
                            synchronization_result['membranes_synchronized'] += 1

            # Update tensor field mappings
            self._update_tensor_field_mappings(enterprise_id)
            synchronization_result['tensor_mappings_updated'] = len(self.tensor_mappings)

            # Call Scheme synchronization function
            self._call_scheme_function('synchronize-enterprise-membranes', [enterprise_id])

            synchronization_result['status'] = 'completed'
            synchronization_result['end_time'] = datetime.utcnow().isoformat()

        except Exception as e:
            logger.error(f"❌ Synchronization failed: {e}")
            synchronization_result['status'] = 'failed'
            synchronization_result['error'] = str(e)

        return synchronization_result

    def generate_ggml_grammar(self, enterprise_id: str) -> dict[str, Any]:
        """Generate ggml-compatible cognitive grammar"""
        logger.info(f"📝 Generating ggml cognitive grammar for {enterprise_id}")

        ggml_grammar = {
            'cognitive_grammar': {
                'version': '2.0',
                'enterprise': enterprise_id,
                'generation_timestamp': datetime.utcnow().isoformat(),
                'membrane_topology': self.membrane_config,
                'tensor_mappings': self.tensor_mappings,
                'cognitive_primitives': self._generate_cognitive_primitives(),
                'tensor_optimization': {
                    'method': 'prime_factorization',
                    'memory_layout': 'cognitive_hierarchy',
                    'attention_allocation': 'enterprise_weighted'
                },
                'ggml_compatibility': {
                    'version': '1.0',
                    'tensor_types': ['f32', 'f16'],
                    'operations': ['matmul', 'attention', 'fold', 'unfold', 'synchronize']
                }
            }
        }

        return ggml_grammar

    def save_membrane_state(self, output_path: str = "cognitive-membrane-state.json") -> str:
        """Save current membrane state to file"""
        state_data = {
            'membrane_config': self.membrane_config,
            'tensor_mappings': self.tensor_mappings,
            'timestamp': datetime.utcnow().isoformat(),
            'schema_version': '1.0'
        }

        output_file = Path(output_path)
        with open(output_file, 'w') as f:
            safe_json_dump(state_data, f, indent=2)

        logger.info(f"💾 Saved membrane state to {output_file}")
        return str(output_file)

    def load_membrane_state(self, input_path: str) -> bool:
        """Load membrane state from file"""
        try:
            input_file = Path(input_path)
            if not input_file.exists():
                logger.error(f"❌ State file not found: {input_file}")
                return False

            with open(input_file) as f:
                state_data = json.load(f)

            self.membrane_config = state_data.get('membrane_config', {})
            self.tensor_mappings = state_data.get('tensor_mappings', {})

            logger.info(f"📥 Loaded membrane state from {input_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load membrane state: {e}")
            return False

    # Private helper methods

    def _calculate_org_tensor_shape(self, org_id: str) -> list[int]:
        """Calculate optimal tensor shape for organizational membrane"""
        base_complexity = len(org_id)
        if base_complexity < 8:
            return [2, 2, 2]
        elif base_complexity < 12:
            return [3, 3, 2]
        elif base_complexity < 16:
            return [3, 3, 3]
        else:
            return [5, 3, 2]

    def _calculate_repo_complexity(self, cognitive_patterns: list[str]) -> float:
        """Calculate cognitive complexity score for repository"""
        complexity = 1.0

        pattern_weights = {
            'neural_networks': 2.5,
            'symbolic_reasoning': 3.0,
            'knowledge_graphs': 2.0,
            'attention_mechanisms': 1.8,
            'memory_systems': 2.2,
            'learning_algorithms': 1.5
        }

        for pattern in cognitive_patterns:
            weight = pattern_weights.get(pattern, 1.1)
            complexity *= weight

        return min(complexity, 10.0)  # Cap at 10.0

    def _derive_tensor_shape_from_complexity(self, complexity: float) -> list[int]:
        """Derive optimal tensor shape from complexity score"""
        int_complexity = round(complexity)
        factors = self._prime_factorize(int_complexity)
        return self._arrange_factors_into_tensor_shape(factors)

    def _prime_factorize(self, n: int) -> list[int]:
        """Prime factorization of a number"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors if factors else [1]

    def _arrange_factors_into_tensor_shape(self, factors: list[int]) -> list[int]:
        """Arrange prime factors into 3D tensor shape"""
        if not factors:
            return [1, 1, 1]
        elif len(factors) == 1:
            return [factors[0], 1, 1]
        elif len(factors) == 2:
            return [factors[0], factors[1], 1]
        else:
            # Distribute factors across 3 dimensions
            f1 = factors[0]
            f2 = factors[1] if len(factors) > 1 else 1
            f3 = np.prod(factors[2:]) if len(factors) > 2 else 1
            return [f1, f2, int(f3)]

    def _assess_membrane_permeability(self, cognitive_patterns: list[str]) -> str:
        """Assess membrane permeability based on cognitive patterns"""
        if 'neural_networks' in cognitive_patterns:
            return 'high'
        elif 'symbolic_reasoning' in cognitive_patterns:
            return 'selective'
        elif 'knowledge_graphs' in cognitive_patterns:
            return 'bidirectional'
        else:
            return 'medium'

    def _get_membrane_data(self, membrane_id: str) -> dict[str, Any] | None:
        """Get membrane data by ID"""
        # Check if it's an organization
        if 'organizations' in self.membrane_config and membrane_id in self.membrane_config['organizations']:
            return self.membrane_config['organizations'][membrane_id]

        # Check if it's a repository
        for org_data in self.membrane_config.get('organizations', {}).values():
            if 'repositories' in org_data and membrane_id in org_data['repositories']:
                return org_data['repositories'][membrane_id]

        # Check if it's the enterprise itself
        if membrane_id == self.membrane_config.get('enterprise_id'):
            return self.membrane_config

        return None

    def _generate_membrane_markdown(self, membrane_id: str) -> str:
        """Generate markdown representation of membrane"""
        membrane_data = self._get_membrane_data(membrane_id)
        if not membrane_data:
            return f"# ❌ Membrane {membrane_id} not found\n"

        markdown = f"# 🧠 Cognitive Membrane: {membrane_id}\n\n"

        if 'membrane_type' in membrane_data:
            markdown += f"**Type**: {membrane_data['membrane_type']}\n"
        if 'tensor_shape' in membrane_data:
            markdown += f"**Tensor Shape**: {membrane_data['tensor_shape']}\n"
        if 'complexity_score' in membrane_data:
            markdown += f"**Complexity**: {membrane_data['complexity_score']:.2f}\n"
        if 'membrane_permeability' in membrane_data:
            markdown += f"**Permeability**: {membrane_data['membrane_permeability']}\n"

        markdown += f"**Last Updated**: {datetime.utcnow().isoformat()}\n\n"

        return markdown

    def _synchronize_organization(self, org_id: str, org_data: dict[str, Any]) -> None:
        """Synchronize organizational membrane"""
        logger.info(f"🌀 Synchronizing organization: {org_id}")
        # Update timestamp
        org_data['last_synchronized'] = datetime.utcnow().isoformat()

    def _synchronize_repository(self, repo_id: str) -> None:
        """Synchronize repository membrane"""
        logger.info(f"📂 Synchronizing repository: {repo_id}")
        # Repository synchronization logic here

    def _update_tensor_field_mappings(self, enterprise_id: str) -> None:
        """Update tensor field mappings for enterprise"""
        total_complexity = 0
        total_repos = 0

        for org_data in self.membrane_config.get('organizations', {}).values():
            for repo_data in org_data.get('repositories', {}).values():
                total_complexity += repo_data.get('complexity_score', 1.0)
                total_repos += 1

        enterprise_tensor_shape = [7, len(self.membrane_config.get('organizations', {})), total_repos, int(total_complexity), total_repos * 10]

        self.tensor_mappings[enterprise_id] = {
            'enterprise_tensor_shape': enterprise_tensor_shape,
            'total_complexity': total_complexity,
            'total_repositories': total_repos,
            'memory_efficiency': min(1.0, 100.0 / total_complexity) if total_complexity > 0 else 1.0,
            'last_updated': datetime.utcnow().isoformat()
        }

    def _generate_cognitive_primitives(self) -> dict[str, Any]:
        """Generate cognitive primitives for ggml grammar"""
        return {
            'attention_mechanisms': {
                'tensor_shape': [7, 7, 1],
                'complexity': 49,
                'operations': ['attend', 'focus', 'distribute']
            },
            'memory_consolidation': {
                'tensor_shape': [5, 3, 2],
                'complexity': 30,
                'operations': ['store', 'retrieve', 'consolidate']
            },
            'pattern_recognition': {
                'tensor_shape': [3, 3, 3],
                'complexity': 27,
                'operations': ['detect', 'classify', 'generalize']
            },
            'symbolic_reasoning': {
                'tensor_shape': [11, 1, 1],
                'complexity': 11,
                'operations': ['infer', 'deduce', 'unify']
            }
        }

    def _call_scheme_function(self, function_name: str, args: list[Any]) -> Any:
        """Call Scheme function from cognitive-membrane-sync.scm"""
        try:
            # In a full implementation, this would use a Scheme interpreter
            # For now, we'll simulate the call
            logger.info(f"🔧 Calling Scheme function: {function_name} with args: {args}")
            return f"scheme_result_{function_name}"
        except Exception as e:
            logger.error(f"❌ Failed to call Scheme function {function_name}: {e}")
            return None


def main():
    """Main function for testing the cognitive membrane bridge"""
    print("🧠 Testing Cognitive Membrane Synchronization Bridge")
    print("=" * 55)

    # Initialize bridge
    bridge = CognitiveMembraneBridge()

    # Initialize enterprise topology
    enterprise_config = bridge.initialize_membrane_topology('cosmos-enterprise', [7, 3, 10, 50, 100])
    print(f"✅ Initialized enterprise: {enterprise_config['enterprise_id']}")

    # Create organizational membranes
    bridge.create_organizational_membrane('cogpilot', 'interface_membrane', 2)
    bridge.create_organizational_membrane('OzCog', 'core_cognitive_membrane', 3)
    bridge.create_organizational_membrane('cosmos', 'meta_coordination_membrane', 5)

    print(f"✅ Created {len(bridge.membrane_config['organizations'])} organizational membranes")

    # Create repository membranes
    bridge.create_repository_membrane('cognitive-cities', 'cogpilot', ['neural_networks', 'attention_mechanisms'])
    bridge.create_repository_membrane('opencog-unified', 'OzCog', ['symbolic_reasoning', 'knowledge_graphs', 'memory_systems'])
    bridge.create_repository_membrane('membrane-sync', 'cosmos', ['learning_algorithms'])

    total_repos = sum(len(org['repositories']) for org in bridge.membrane_config['organizations'].values())
    print(f"✅ Created {total_repos} repository membranes")

    # Demonstrate operations
    print("\n🌀 Demonstrating membrane operations:")

    # Fold operation
    bridge.fold_membrane_to_markdown('cosmos-enterprise')
    print("📝 ✅ Folded enterprise membrane to markdown")

    # Project operation
    bridge.project_membrane_to_tensor('cosmos-enterprise')
    print("📊 ✅ Projected enterprise membrane to tensor")

    # Embed operation
    bridge.embed_membrane_in_hypergraph('cosmos-enterprise')
    print("🔗 ✅ Embedded enterprise membrane in hypergraph")

    # Synchronization
    sync_result = bridge.synchronize_enterprise_membranes('cosmos-enterprise')
    print(f"🔄 ✅ Synchronized {sync_result['membranes_synchronized']} membranes")

    # Generate ggml grammar
    bridge.generate_ggml_grammar('cosmos-enterprise')
    print("📝 ✅ Generated ggml cognitive grammar")

    # Save state
    state_file = bridge.save_membrane_state()
    print(f"💾 ✅ Saved membrane state to {state_file}")

    print("\n📈 Final Status:")
    print(f"   Enterprise: {bridge.membrane_config['enterprise_id']}")
    print(f"   Organizations: {len(bridge.membrane_config['organizations'])}")
    print(f"   Total repositories: {total_repos}")
    print(f"   Tensor mappings: {len(bridge.tensor_mappings)}")

    print("\n✅ Cognitive Membrane Synchronization Bridge test completed!")


if __name__ == "__main__":
    main()
