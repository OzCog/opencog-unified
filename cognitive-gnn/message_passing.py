#!/usr/bin/env python3
"""
Neural Message Passing Implementation
Phase α: GraphQL-GNN Foundation

Implements 7-layer parallel message passing with attention modulation
for the 343-state neural graph network.

Copyright (c) 2025 OpenCog Foundation
"""

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import numpy as np


@dataclass
class GraphNode:
    """Neural graph node representation"""

    id: str
    embedding: np.ndarray
    coordinates: tuple[int, int, int]
    attention_score: float = 0.5
    layer: int = 0


@dataclass
class GraphEdge:
    """Neural graph edge representation"""

    id: str
    source: str
    target: str
    weight: float
    message_vector: np.ndarray
    attention_weight: float = 1.0


@dataclass
class NeuralGraph:
    """Complete neural graph structure"""

    nodes: dict[str, GraphNode]
    edges: dict[str, GraphEdge]
    tensor_shape: tuple[int, int, int] = (7, 7, 7)
    current_state: int = 0
    attention_matrix: np.ndarray = None

    def __post_init__(self):
        if self.attention_matrix is None:
            self.attention_matrix = np.eye(7)  # Default attention matrix


class MessagePassingEngine:
    """
    Neural message passing engine with 7-layer architecture

    Implements parallel message passing across the 7×7×7 tensor space
    with attention modulation at each layer.
    """

    def __init__(self, embedding_dim: int = 64):
        self.embedding_dim = embedding_dim
        self.num_layers = 7
        self.attention_heads = 7
        self.message_passes = 7

        # Initialize layer-specific weight matrices
        self.layer_weights = {}
        self.attention_weights = {}

        for layer in range(self.num_layers):
            self.layer_weights[layer] = np.random.randn(embedding_dim, embedding_dim) * 0.1
            self.attention_weights[layer] = np.random.randn(7, 7) * 0.1

        # Thread safety
        self.lock = threading.Lock()

    def neural_propagation(self, graph: NeuralGraph, query_embedding: np.ndarray | None = None) -> NeuralGraph:
        """
        Perform neural propagation across 7 layers with attention modulation

        Args:
            graph: Input neural graph
            query_embedding: Optional query embedding for guided propagation

        Returns:
            NeuralGraph: Updated graph after propagation
        """
        updated_graph = self._deep_copy_graph(graph)

        # Perform 7 layers of message passing
        for layer in range(self.num_layers):
            print(f"Processing layer {layer + 1}/7...")
            updated_graph = self._message_pass_layer(updated_graph, layer, query_embedding)

            # Update attention scores based on layer processing
            self._update_attention_scores(updated_graph, layer)

        # Reshape final embeddings to 7×7×7 tensor structure
        self._reshape_to_tensor(updated_graph)

        return updated_graph

    def _message_pass_layer(
        self, graph: NeuralGraph, layer: int, query_embedding: np.ndarray | None = None
    ) -> NeuralGraph:
        """
        Perform message passing for a single layer

        Args:
            graph: Neural graph
            layer: Current layer index (0-6)
            query_embedding: Optional query context

        Returns:
            NeuralGraph: Graph with updated embeddings for this layer
        """
        # Collect messages for all nodes in parallel
        node_messages = {}

        # Use ThreadPoolExecutor for parallel message computation
        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = {}

            for node_id, _node in graph.nodes.items():
                future = executor.submit(self._compute_node_messages, graph, node_id, layer, query_embedding)
                futures[node_id] = future

            # Collect results
            for node_id, future in futures.items():
                node_messages[node_id] = future.result()

        # Apply messages to update node embeddings
        for node_id, messages in node_messages.items():
            if messages:
                aggregated_message = self._aggregate_messages(messages, layer)
                self._update_node_embedding(graph.nodes[node_id], aggregated_message, layer)

        return graph

    def _compute_node_messages(
        self, graph: NeuralGraph, node_id: str, layer: int, query_embedding: np.ndarray | None = None
    ) -> list[np.ndarray]:
        """
        Compute incoming messages for a specific node

        Args:
            graph: Neural graph
            node_id: Target node ID
            layer: Current layer
            query_embedding: Optional query context

        Returns:
            List[np.ndarray]: List of message vectors
        """
        messages = []
        target_node = graph.nodes[node_id]

        # Find all incoming edges
        for _edge_id, edge in graph.edges.items():
            if edge.target == node_id:
                source_node = graph.nodes[edge.source]

                # Compute message from source to target
                message = self._compute_message(source_node, target_node, edge, layer, query_embedding)

                # Apply attention weighting
                attention_weight = self._compute_attention_weight(source_node, target_node, layer)

                weighted_message = message * attention_weight
                messages.append(weighted_message)

        return messages

    def _compute_message(
        self,
        source: GraphNode,
        target: GraphNode,
        edge: GraphEdge,
        layer: int,
        query_embedding: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Compute message vector between two nodes

        Args:
            source: Source node
            target: Target node
            edge: Connecting edge
            layer: Current layer
            query_embedding: Optional query context

        Returns:
            np.ndarray: Message vector
        """
        # Apply layer-specific weight transformation
        layer_weights = self.layer_weights[layer]
        transformed_embedding = layer_weights @ source.embedding

        # Apply edge weight
        message = transformed_embedding * edge.weight

        # Add query context if provided
        if query_embedding is not None:
            # Compute attention between source embedding and query
            query_attention = (
                np.dot(source.embedding, query_embedding)
                / np.linalg.norm(source.embedding)
                / np.linalg.norm(query_embedding)
            )
            message *= 1.0 + query_attention

        # Apply positional encoding based on coordinates
        pos_encoding = self._positional_encoding(source.coordinates, target.coordinates)
        message += pos_encoding

        return message

    def _compute_attention_weight(self, source: GraphNode, target: GraphNode, layer: int) -> float:
        """
        Compute attention weight between two nodes for given layer

        Args:
            source: Source node
            target: Target node
            layer: Current layer

        Returns:
            float: Attention weight
        """
        # Get coordinate-based attention
        src_x, src_y, src_z = source.coordinates
        tgt_x, tgt_y, tgt_z = target.coordinates

        # Distance-based attention (closer nodes have higher attention)
        coord_distance = np.sqrt((src_x - tgt_x) ** 2 + (src_y - tgt_y) ** 2 + (src_z - tgt_z) ** 2)
        distance_attention = 1.0 / (1.0 + coord_distance)

        # Layer-specific attention weights
        layer_attention = self.attention_weights[layer][src_x % 7, tgt_x % 7]

        # Combine attention sources
        combined_attention = distance_attention * np.exp(layer_attention)

        # Apply softmax normalization within reasonable bounds
        return min(max(combined_attention, 0.01), 2.0)

    def _positional_encoding(
        self, source_coords: tuple[int, int, int], target_coords: tuple[int, int, int]
    ) -> np.ndarray:
        """
        Generate positional encoding based on 3D coordinates

        Args:
            source_coords: Source node coordinates
            target_coords: Target node coordinates

        Returns:
            np.ndarray: Positional encoding vector
        """
        encoding = np.zeros(self.embedding_dim)

        # Compute relative position
        rel_x = target_coords[0] - source_coords[0]
        rel_y = target_coords[1] - source_coords[1]
        rel_z = target_coords[2] - source_coords[2]

        # Generate sinusoidal encoding for each dimension
        for i in range(self.embedding_dim // 3):
            if i * 3 < self.embedding_dim:
                encoding[i * 3] = np.sin(rel_x / (10000 ** (2 * i / self.embedding_dim))) * 0.1
            if i * 3 + 1 < self.embedding_dim:
                encoding[i * 3 + 1] = np.cos(rel_y / (10000 ** (2 * i / self.embedding_dim))) * 0.1
            if i * 3 + 2 < self.embedding_dim:
                encoding[i * 3 + 2] = np.sin(rel_z / (10000 ** (2 * i / self.embedding_dim))) * 0.1

        return encoding

    def _aggregate_messages(self, messages: list[np.ndarray], layer: int) -> np.ndarray:
        """
        Aggregate multiple message vectors

        Args:
            messages: List of message vectors
            layer: Current layer

        Returns:
            np.ndarray: Aggregated message
        """
        if not messages:
            return np.zeros(self.embedding_dim)

        # Simple mean aggregation with layer-specific weighting
        aggregated = np.mean(messages, axis=0)

        # Apply layer-specific activation
        layer_factor = (layer + 1) / self.num_layers
        activated = np.tanh(aggregated * layer_factor)

        return activated

    def _update_node_embedding(self, node: GraphNode, message: np.ndarray, layer: int) -> None:
        """
        Update node embedding with received message

        Args:
            node: Node to update
            message: Aggregated message
            layer: Current layer
        """
        # Residual connection
        update_rate = 0.1 * (layer + 1) / self.num_layers
        node.embedding = (1 - update_rate) * node.embedding + update_rate * message

        # Normalize to prevent explosion
        norm = np.linalg.norm(node.embedding)
        if norm > 1e-6:
            node.embedding = node.embedding / norm

        # Update layer information
        node.layer = layer

    def _update_attention_scores(self, graph: NeuralGraph, layer: int) -> None:
        """
        Update attention scores for all nodes based on layer processing

        Args:
            graph: Neural graph
            layer: Current layer
        """
        for node in graph.nodes.values():
            # Compute attention score based on embedding magnitude and position
            embedding_magnitude = np.linalg.norm(node.embedding)

            # Position-based attention (center positions get higher attention)
            center_distance = np.sqrt(sum((c - 3) ** 2 for c in node.coordinates))
            position_attention = 1.0 / (1.0 + center_distance)

            # Combine factors
            node.attention_score = 0.7 * embedding_magnitude + 0.3 * position_attention

            # Clamp to valid range
            node.attention_score = max(0.0, min(1.0, node.attention_score))

    def _reshape_to_tensor(self, graph: NeuralGraph) -> None:
        """
        Reshape final embeddings to maintain 7×7×7 tensor structure

        Args:
            graph: Neural graph to reshape
        """
        # Update current state based on dominant node
        max_attention_node = max(graph.nodes.values(), key=lambda n: n.attention_score)

        # Compute state index from coordinates
        x, y, z = max_attention_node.coordinates
        graph.current_state = x * 49 + y * 7 + z

        # Update attention matrix based on node attentions
        for node in graph.nodes.values():
            x, y, z = node.coordinates
            if x < 7 and y < 7:  # Ensure within bounds
                graph.attention_matrix[x, y] = node.attention_score

    def _deep_copy_graph(self, graph: NeuralGraph) -> NeuralGraph:
        """Create a deep copy of the neural graph"""
        new_nodes = {}
        new_edges = {}

        # Copy nodes
        for node_id, node in graph.nodes.items():
            new_nodes[node_id] = GraphNode(
                id=node.id,
                embedding=node.embedding.copy(),
                coordinates=node.coordinates,
                attention_score=node.attention_score,
                layer=node.layer,
            )

        # Copy edges
        for edge_id, edge in graph.edges.items():
            new_edges[edge_id] = GraphEdge(
                id=edge.id,
                source=edge.source,
                target=edge.target,
                weight=edge.weight,
                message_vector=edge.message_vector.copy(),
                attention_weight=edge.attention_weight,
            )

        return NeuralGraph(
            nodes=new_nodes,
            edges=new_edges,
            tensor_shape=graph.tensor_shape,
            current_state=graph.current_state,
            attention_matrix=graph.attention_matrix.copy(),
        )

    def create_test_graph(self) -> NeuralGraph:
        """
        Create a test graph with 7×7×7 structure for validation

        Returns:
            NeuralGraph: Test graph with 343 nodes
        """
        nodes = {}
        edges = {}

        # Create nodes for each position in 7×7×7 tensor
        node_count = 0
        for x in range(7):
            for y in range(7):
                for z in range(7):
                    node_id = f"node_{x}_{y}_{z}"

                    # Generate random embedding
                    embedding = np.random.randn(self.embedding_dim) * 0.1
                    embedding = embedding / np.linalg.norm(embedding)

                    nodes[node_id] = GraphNode(
                        id=node_id, embedding=embedding, coordinates=(x, y, z), attention_score=0.5, layer=0
                    )
                    node_count += 1

        # Create edges between adjacent nodes
        edge_count = 0
        for x in range(7):
            for y in range(7):
                for z in range(7):
                    current_id = f"node_{x}_{y}_{z}"

                    # Connect to adjacent nodes (6-connectivity)
                    for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                        nx, ny, nz = x + dx, y + dy, z + dz

                        if 0 <= nx < 7 and 0 <= ny < 7 and 0 <= nz < 7:
                            neighbor_id = f"node_{nx}_{ny}_{nz}"
                            edge_id = f"edge_{edge_count}"

                            # Random edge weight
                            weight = np.random.uniform(0.1, 1.0)

                            edges[edge_id] = GraphEdge(
                                id=edge_id,
                                source=current_id,
                                target=neighbor_id,
                                weight=weight,
                                message_vector=np.zeros(self.embedding_dim),
                                attention_weight=1.0,
                            )
                            edge_count += 1

        print(f"Created test graph with {node_count} nodes and {edge_count} edges")

        return NeuralGraph(
            nodes=nodes, edges=edges, tensor_shape=(7, 7, 7), current_state=0, attention_matrix=np.eye(7)
        )


def main():
    """Test the message passing engine"""
    print("=== Neural Message Passing Engine Test ===")

    # Create engine
    engine = MessagePassingEngine(embedding_dim=64)

    # Create test graph
    print("\nCreating test graph...")
    graph = engine.create_test_graph()

    print(f"Graph nodes: {len(graph.nodes)}")
    print(f"Graph edges: {len(graph.edges)}")
    print(f"Tensor shape: {graph.tensor_shape}")

    # Test message passing
    print("\nPerforming neural propagation...")
    updated_graph = engine.neural_propagation(graph)

    print(f"Final state: {updated_graph.current_state}")

    # Analyze results
    attention_scores = [node.attention_score for node in updated_graph.nodes.values()]
    print("\nAttention statistics:")
    print(f"  Mean: {np.mean(attention_scores):.4f}")
    print(f"  Std:  {np.std(attention_scores):.4f}")
    print(f"  Min:  {np.min(attention_scores):.4f}")
    print(f"  Max:  {np.max(attention_scores):.4f}")

    # Find top attention nodes
    top_nodes = sorted(updated_graph.nodes.values(), key=lambda n: n.attention_score, reverse=True)[:5]

    print("\nTop 5 attention nodes:")
    for i, node in enumerate(top_nodes):
        print(f"  {i + 1}. {node.id}: attention={node.attention_score:.4f}, coords={node.coordinates}")

    # Validate 343 states
    total_states = len(updated_graph.nodes)
    print("\nState validation:")
    print(f"  Total nodes: {total_states}")
    print("  Expected (7³): 343")
    print(f"  Validation: {'✅ PASS' if total_states == 343 else '❌ FAIL'}")

    # Save results
    results = {
        "total_nodes": len(updated_graph.nodes),
        "total_edges": len(updated_graph.edges),
        "tensor_shape": updated_graph.tensor_shape,
        "current_state": updated_graph.current_state,
        "attention_statistics": {
            "mean": float(np.mean(attention_scores)),
            "std": float(np.std(attention_scores)),
            "min": float(np.min(attention_scores)),
            "max": float(np.max(attention_scores)),
        },
        "validation": {"expected_states": 343, "actual_states": total_states, "passed": total_states == 343},
    }

    with open("message_passing_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== Results saved to message_passing_results.json ===")


if __name__ == "__main__":
    main()
