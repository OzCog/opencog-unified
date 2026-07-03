import numpy as np
import torch
import json
import yaml
import os
import sys
from datetime import datetime
from pathlib import Path
from github import Github

# Enhanced JSON encoder for NumPy types (NumPy 2.0 compatible)
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Removed deprecated np.int_ and np.float_ for NumPy 2.0 compatibility
        if isinstance(obj, (np.integer, np.intc, np.intp, np.int8,
                           np.int16, np.int32, np.int64,
                           np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return obj.item()
        return super().default(obj)

class CognitiveMembrane:
    def __init__(self, enterprise="cosmos"):
        self.enterprise = enterprise
        self.tensor_shape = []
        self.attention_weights = {}
        self.membrane_state = {}
        self.topology = {}

    def fold_enterprise(self, level='enterprise'):
        """Collapse higher dimensions into markdown representation"""
        print(f"🌀 Folding enterprise '{self.enterprise}' at level: {level}")

        # {cosmos} → (org) → [repo] → fold/ → file.md
        membrane_state = self.scan_topology()
        self.generate_markdown_projection(membrane_state)
        return membrane_state

    def unfold_changes(self):
        """Expand markdown changes back to enterprise topology"""
        print("🌊 Unfolding changes across cognitive membrane layers")

        # file.md → fold/ → [repo] → (org) → {cosmos}
        changes = self.detect_membrane_mutations()
        self.propagate_through_layers(changes)
        return changes

    def scan_topology(self):
        """Scan the current cognitive topology"""
        topology = {
            'enterprise': self.enterprise,
            'timestamp': datetime.utcnow().isoformat(),
            'organizations': {},
            'tensor_dimensions': self.calculate_tensor_dimensions(),
            'cognitive_state': 'scanning'
        }

        # Simulate organization scanning for now
        # In full implementation, would use GitHub GraphQL API
        orgs = ['cogpilot', 'OzCog', 'cosmos']
        for org in orgs:
            topology['organizations'][org] = {
                'prime': self.get_org_prime(org),
                'repositories': self.scan_org_repos(org),
                'cognitive_weight': np.random.random()
            }

        self.topology = topology
        return topology

    def get_org_prime(self, org):
        """Assign prime numbers to organizations for tensor factorization"""
        primes = {'cogpilot': 2, 'OzCog': 3, 'cosmos': 5}
        return primes.get(org, 7)

    def scan_org_repos(self, org):
        """Scan repositories within an organization"""
        # Simulate repository scanning
        repo_configs = {
            'cogpilot': ['cognitive-cities', 'plan9-cogcities-kernel'],
            'OzCog': ['opencog-unified', 'opencog-bridge'],
            'cosmos': ['membrane-sync', 'cognitive-grammar']
        }

        repos = {}
        for repo_name in repo_configs.get(org, []):
            repos[repo_name] = {
                'shape': self.calculate_repo_shape(repo_name),
                'cognitive_fragments': self.identify_cognitive_fragments(repo_name),
                'membrane_permeability': 'bidirectional'
            }
        return repos

    def calculate_repo_shape(self, repo_name):
        """Calculate tensor shape for repository based on cognitive complexity"""
        # Simple heuristic based on repo characteristics
        base_shape = [3, 3, 3]  # Default cognitive shape

        if 'cognitive' in repo_name:
            base_shape = [5, 3, 2]
        elif 'opencog' in repo_name:
            base_shape = [7, 2, 1]
        elif 'kernel' in repo_name:
            base_shape = [2, 2, 2]

        return base_shape

    def identify_cognitive_fragments(self, repo_name):
        """Identify fundamental cognitive grammar fragments"""
        fragments = {
            'neural_transport': [3, 3, 3],
            'knowledge_base': [5, 2, 1],
            'governance': [2, 2, 2],
            'protocol_design': [7, 1, 1]
        }

        # Select fragments based on repo characteristics
        if 'cognitive' in repo_name:
            return {'neural_transport': fragments['neural_transport'],
                   'knowledge_base': fragments['knowledge_base']}
        elif 'opencog' in repo_name:
            return {'knowledge_base': fragments['knowledge_base'],
                   'protocol_design': fragments['protocol_design']}
        else:
            return {'governance': fragments['governance']}

    def calculate_tensor_dimensions(self):
        """Calculate tensor dimensions for the enterprise"""
        # [attention, orgs, repos, concepts, implementations]
        dimensions = [7, 3, 10, 50, 100]
        return dimensions

    def generate_markdown_projection(self, membrane_state):
        """Generate markdown projection of the cognitive membrane"""
        markdown_content = f"""# 🌌 {self.enterprise.title()} Enterprise Cognitive Map

## Tensor Dimensions: {membrane_state['tensor_dimensions']}

Generated: {membrane_state['timestamp']}

"""

        for org_name, org_data in membrane_state['organizations'].items():
            markdown_content += f"### ({org_name}) - Prime: {org_data['prime']}\n"

            for repo_name, repo_data in org_data['repositories'].items():
                shape_str = "×".join(map(str, repo_data['shape']))
                markdown_content += f"#### [{repo_name}] - Shape: [{shape_str}]\n"

                for fragment_name, fragment_shape in repo_data['cognitive_fragments'].items():
                    fragment_str = "×".join(map(str, fragment_shape))
                    markdown_content += f"- {fragment_name}.md - Tensor: [{fragment_str}]\n"

            markdown_content += "\n"

        # Save markdown projection
        Path('cosmos-cognitive-index.md').write_text(markdown_content)
        print(f"📝 Generated cognitive index: cosmos-cognitive-index.md")

    def detect_membrane_mutations(self):
        """Detect changes in the cognitive membrane"""
        return {
            'mutations_detected': 0,
            'propagation_paths': [],
            'timestamp': datetime.utcnow().isoformat()
        }

    def propagate_through_layers(self, changes):
        """Propagate changes through cognitive layers"""
        print(f"🌊 Propagating {changes['mutations_detected']} mutations")

    def generate_ggml_tensor_config(self):
        """Generate ggml tensor configuration"""
        config = {
            'tensor_field': self.topology,
            'shape_optimization': 'prime_factorization',
            'memory_layout': 'cognitive_hierarchy',
            'attention_weights': self.attention_weights
        }

        with open('cognitive-grammar.ggml', 'w') as f:
            json.dump(config, f, indent=2, cls=EnhancedJSONEncoder)

        return config

# Execute cognitive membrane operations
if __name__ == "__main__":
    enterprise = os.getenv('INPUT_ENTERPRISE', 'cosmos')
    cognitive_mode = os.getenv('INPUT_COGNITIVE_MODE', 'fold')

    print(f"🧠 Initializing Cognitive Membrane for {enterprise}")
    membrane = CognitiveMembrane(enterprise)

    if cognitive_mode == 'fold':
        membrane_state = membrane.fold_enterprise()
    elif cognitive_mode == 'unfold':
        changes = membrane.unfold_changes()
    elif cognitive_mode == 'project':
        membrane_state = membrane.fold_enterprise('projection')
    elif cognitive_mode == 'embed':
        membrane_state = membrane.fold_enterprise('embedding')

    # Generate ggml configuration
    ggml_config = membrane.generate_ggml_tensor_config()

    print("✅ Cognitive membrane synchronization completed")
