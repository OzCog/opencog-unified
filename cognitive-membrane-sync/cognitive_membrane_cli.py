#!/usr/bin/env python3
"""
Cognitive Membrane Synchronization CLI
Command-line interface for the Multi-Scale Synchronization Framework
"""

import argparse
import sys
from pathlib import Path

from json_encoder_utils import safe_json_dump
from membrane_bridge import CognitiveMembraneBridge


def main():
    parser = argparse.ArgumentParser(
        description='🧠 Cognitive Membrane Synchronization Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init cosmos --tensor-dims 7,3,10,50,100
  %(prog)s create-org cogpilot --type interface_membrane --prime 2
  %(prog)s create-repo cognitive-cities --org cogpilot --patterns neural_networks,attention_mechanisms
  %(prog)s fold cosmos-enterprise
  %(prog)s sync cosmos-enterprise
  %(prog)s status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize enterprise membrane')
    init_parser.add_argument('enterprise_id', help='Enterprise identifier')
    init_parser.add_argument('--tensor-dims', default='7,3,10,50,100',
                           help='Tensor dimensions (comma-separated)')

    # Create organization command
    org_parser = subparsers.add_parser('create-org', help='Create organizational membrane')
    org_parser.add_argument('org_id', help='Organization identifier')
    org_parser.add_argument('--type', default='general_membrane', help='Membrane type')
    org_parser.add_argument('--prime', type=int, default=2, help='Prime factor')

    # Create repository command
    repo_parser = subparsers.add_parser('create-repo', help='Create repository membrane')
    repo_parser.add_argument('repo_id', help='Repository identifier')
    repo_parser.add_argument('--org', required=True, help='Parent organization')
    repo_parser.add_argument('--patterns', default='', help='Cognitive patterns (comma-separated)')

    # Fold command
    fold_parser = subparsers.add_parser('fold', help='Fold membrane to markdown')
    fold_parser.add_argument('membrane_id', help='Membrane identifier')

    # Unfold command
    unfold_parser = subparsers.add_parser('unfold', help='Unfold markdown to membrane')
    unfold_parser.add_argument('markdown_file', help='Markdown file path')
    unfold_parser.add_argument('membrane_id', help='Target membrane identifier')

    # Project command
    project_parser = subparsers.add_parser('project', help='Project membrane to tensor')
    project_parser.add_argument('membrane_id', help='Membrane identifier')

    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Embed membrane in hypergraph')
    embed_parser.add_argument('membrane_id', help='Membrane identifier')

    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Synchronize enterprise membranes')
    sync_parser.add_argument('enterprise_id', help='Enterprise identifier')

    # Status command
    subparsers.add_parser('status', help='Show membrane status')

    # Generate ggml command
    ggml_parser = subparsers.add_parser('ggml', help='Generate ggml grammar')
    ggml_parser.add_argument('enterprise_id', help='Enterprise identifier')

    # Save/Load commands
    save_parser = subparsers.add_parser('save', help='Save membrane state')
    save_parser.add_argument('--output', default='cognitive-membrane-state.json', help='Output file')

    load_parser = subparsers.add_parser('load', help='Load membrane state')
    load_parser.add_argument('input_file', help='Input file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize bridge
    bridge = CognitiveMembraneBridge()

    try:
        if args.command == 'init':
            tensor_dims = [int(x.strip()) for x in args.tensor_dims.split(',')]
            config = bridge.initialize_membrane_topology(args.enterprise_id, tensor_dims)
            print(f"✅ Initialized enterprise: {config['enterprise_id']}")
            print(f"   Tensor dimensions: {config['tensor_dimensions']}")

        elif args.command == 'create-org':
            membrane = bridge.create_organizational_membrane(args.org_id, args.type, args.prime)
            print(f"✅ Created organizational membrane: {args.org_id}")
            print(f"   Type: {membrane['membrane_type']}")
            print(f"   Prime factor: {membrane['prime_factor']}")

        elif args.command == 'create-repo':
            patterns = [p.strip() for p in args.patterns.split(',') if p.strip()]
            membrane = bridge.create_repository_membrane(args.repo_id, args.org, patterns)
            print(f"✅ Created repository membrane: {args.repo_id}")
            print(f"   Organization: {membrane['org_id']}")
            print(f"   Patterns: {membrane['cognitive_patterns']}")
            print(f"   Complexity: {membrane['complexity_score']:.2f}")

        elif args.command == 'fold':
            bridge.fold_membrane_to_markdown(args.membrane_id)
            print(f"✅ Folded membrane {args.membrane_id} to markdown")
            print(f"   Output: cognitive-membrane-{args.membrane_id}.md")

        elif args.command == 'unfold':
            if not Path(args.markdown_file).exists():
                print(f"❌ File not found: {args.markdown_file}")
                return 1
            with open(args.markdown_file) as f:
                markdown_content = f.read()
            success = bridge.unfold_membrane_from_markdown(markdown_content, args.membrane_id)
            if success:
                print(f"✅ Unfolded markdown into membrane {args.membrane_id}")
            else:
                print(f"❌ Failed to unfold markdown into membrane {args.membrane_id}")

        elif args.command == 'project':
            tensor_field = bridge.project_membrane_to_tensor(args.membrane_id)
            if tensor_field is not None:
                print(f"✅ Projected membrane {args.membrane_id} to tensor")
                print(f"   Tensor shape: {tensor_field.shape}")
                print(f"   Output: cognitive-tensor-{args.membrane_id}.npy")
            else:
                print(f"❌ Failed to project membrane {args.membrane_id}")

        elif args.command == 'embed':
            embedding = bridge.embed_membrane_in_hypergraph(args.membrane_id)
            if embedding:
                print(f"✅ Embedded membrane {args.membrane_id} in hypergraph")
                print(f"   Node type: {embedding.get('node_type', 'unknown')}")
                print(f"   Edges: {len(embedding.get('edges', []))}")
            else:
                print(f"❌ Failed to embed membrane {args.membrane_id}")

        elif args.command == 'sync':
            result = bridge.synchronize_enterprise_membranes(args.enterprise_id)
            print(f"✅ Synchronized enterprise: {args.enterprise_id}")
            print(f"   Membranes synchronized: {result['membranes_synchronized']}")
            print(f"   Status: {result['status']}")

        elif args.command == 'status':
            if bridge.membrane_config:
                print("📊 Cognitive Membrane Status")
                print("=" * 30)
                print(f"Enterprise: {bridge.membrane_config.get('enterprise_id', 'None')}")
                print(f"Organizations: {len(bridge.membrane_config.get('organizations', {}))}")

                total_repos = sum(len(org.get('repositories', {}))
                                for org in bridge.membrane_config.get('organizations', {}).values())
                print(f"Repositories: {total_repos}")
                print(f"Tensor mappings: {len(bridge.tensor_mappings)}")

                if bridge.membrane_config.get('organizations'):
                    print("\nOrganizations:")
                    for org_id, org_data in bridge.membrane_config['organizations'].items():
                        print(f"  • {org_id} ({org_data.get('membrane_type', 'unknown')})")
                        for repo_id in org_data.get('repositories', {}):
                            print(f"    - {repo_id}")
            else:
                print("❌ No membrane configuration loaded")

        elif args.command == 'ggml':
            grammar = bridge.generate_ggml_grammar(args.enterprise_id)
            output_file = f"cognitive-grammar-{args.enterprise_id}.ggml"
            with open(output_file, 'w') as f:
                safe_json_dump(grammar, f, indent=2)
            print(f"✅ Generated ggml grammar for {args.enterprise_id}")
            print(f"   Output: {output_file}")

        elif args.command == 'save':
            output_file = bridge.save_membrane_state(args.output)
            print(f"✅ Saved membrane state to {output_file}")

        elif args.command == 'load':
            success = bridge.load_membrane_state(args.input_file)
            if success:
                print(f"✅ Loaded membrane state from {args.input_file}")
            else:
                print(f"❌ Failed to load membrane state from {args.input_file}")
                return 1

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
