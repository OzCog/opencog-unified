"""
GraphQL Query Parser to Graph Structure
Phase α: GraphQL-GNN Foundation

Converts GraphQL queries to neural graph structures for processing
with the 7×7×7 tensor architecture.

Copyright (c) 2025 OpenCog Foundation
"""

import json
import re
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

import numpy as np


class QueryType(Enum):
    QUERY = "query"
    MUTATION = "mutation"
    SUBSCRIPTION = "subscription"

class DirectiveType(Enum):
    NEURAL_ATTENTION = "neural_attention"
    MESSAGE_PASSING = "message_passing"
    TENSOR_RESHAPE = "tensor_reshape"
    COGNITIVE_PRIMITIVE = "cognitive_primitive"

@dataclass
class QueryField:
    """Represents a field in a GraphQL query"""
    name: str
    alias: str | None = None
    arguments: dict[str, Any] = None
    directives: list[dict[str, Any]] = None
    selections: list['QueryField'] = None

    def __post_init__(self):
        if self.arguments is None:
            self.arguments = {}
        if self.directives is None:
            self.directives = []
        if self.selections is None:
            self.selections = []

@dataclass
class ParsedQuery:
    """Complete parsed GraphQL query structure"""
    operation_type: QueryType
    operation_name: str | None
    fields: list[QueryField]
    variables: dict[str, Any] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = {}

@dataclass
class NeuralGraphStructure:
    """Neural graph representation of parsed query"""
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    tensor_shape: tuple[int, int, int] = (7, 7, 7)
    query_embedding: np.ndarray = None
    attention_weights: np.ndarray = None

class GraphQLQueryParser:
    """
    GraphQL Query Parser for Neural Graph Networks

    Converts GraphQL queries into neural graph structures that can be
    processed by the 7×7×7 tensor architecture.
    """

    def __init__(self):
        self.embedding_dim = 64
        self.tensor_shape = (7, 7, 7)

        # Field type mappings for neural processing
        self.field_type_embeddings = {
            "getNeuralGraph": np.array([1, 0, 0, 0]),
            "getAttentionState": np.array([0, 1, 0, 0]),
            "performMessagePassing": np.array([0, 0, 1, 0]),
            "getCognitivePrimitive": np.array([0, 0, 0, 1]),
            "allocateAttention": np.array([1, 1, 0, 0]),
            "updateNeuralWeights": np.array([1, 0, 1, 0]),
            "executeMessagePassing": np.array([0, 1, 1, 0]),
            "attentionUpdates": np.array([1, 1, 1, 0]),
            "neuralStateChanges": np.array([1, 0, 0, 1])
        }

    def parse_query(self, query_string: str) -> ParsedQuery:
        """
        Parse GraphQL query string into structured representation

        Args:
            query_string: GraphQL query string

        Returns:
            ParsedQuery: Parsed query structure
        """
        # Clean and normalize query
        cleaned_query = self._clean_query(query_string)

        # Extract operation type and name
        operation_type, operation_name = self._extract_operation(cleaned_query)

        # Extract variables
        variables = self._extract_variables(cleaned_query)

        # Parse fields
        fields = self._parse_fields(cleaned_query)

        return ParsedQuery(
            operation_type=operation_type,
            operation_name=operation_name,
            fields=fields,
            variables=variables
        )

    def query_to_neural_graph(self, query: str | ParsedQuery) -> NeuralGraphStructure:
        """
        Convert GraphQL query to neural graph structure

        Args:
            query: GraphQL query string or parsed query

        Returns:
            NeuralGraphStructure: Neural graph representation
        """
        if isinstance(query, str):
            parsed_query = self.parse_query(query)
        else:
            parsed_query = query

        # Generate query embedding
        query_embedding = self._generate_query_embedding(parsed_query)

        # Create nodes and edges
        nodes, edges = self._build_graph_structure(parsed_query)

        # Generate attention weights
        attention_weights = self._compute_attention_weights(parsed_query, nodes)

        return NeuralGraphStructure(
            nodes=nodes,
            edges=edges,
            tensor_shape=self.tensor_shape,
            query_embedding=query_embedding,
            attention_weights=attention_weights
        )

    def _clean_query(self, query_string: str) -> str:
        """Clean and normalize GraphQL query string"""
        # Remove comments
        query_string = re.sub(r'#.*$', '', query_string, flags=re.MULTILINE)

        # Normalize whitespace
        query_string = re.sub(r'\s+', ' ', query_string)

        # Remove leading/trailing whitespace
        query_string = query_string.strip()

        return query_string

    def _extract_operation(self, query_string: str) -> tuple[QueryType, str | None]:
        """Extract operation type and name from query"""
        # Match operation pattern (more flexible with whitespace and variables)
        operation_match = re.search(r'(query|mutation|subscription)(?:\s+(\w+))?(?:\s*\([^)]*\))?\s*{', query_string)

        if operation_match:
            operation_type = QueryType(operation_match.group(1))
            operation_name = operation_match.group(2)
        else:
            # Default to query if no explicit operation
            operation_type = QueryType.QUERY
            operation_name = None

        return operation_type, operation_name

    def _extract_variables(self, query_string: str) -> dict[str, Any]:
        """Extract variables from GraphQL query"""
        variables = {}

        # Find variable declarations
        var_match = re.search(r'\(([^)]+)\)', query_string)
        if var_match:
            var_string = var_match.group(1)

            # Parse individual variables
            var_pattern = r'\$(\w+):\s*([^,\s]+)(?:\s*=\s*([^,\s]+))?'
            for match in re.finditer(var_pattern, var_string):
                var_name = match.group(1)
                var_type = match.group(2)
                default_value = match.group(3)

                variables[var_name] = {
                    "type": var_type,
                    "default": default_value
                }

        return variables

    def _parse_fields(self, query_string: str) -> list[QueryField]:
        """Parse fields from GraphQL query"""
        fields = []

        # Find the main selection set
        brace_start = query_string.find('{')
        if brace_start == -1:
            return fields

        # Extract content between outermost braces
        brace_count = 0
        start_pos = brace_start + 1
        end_pos = start_pos

        for i, char in enumerate(query_string[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i
                    break

        selection_set = query_string[start_pos:end_pos]

        # Parse individual fields
        fields = self._parse_selection_set(selection_set)

        return fields

    def _parse_selection_set(self, selection_set: str) -> list[QueryField]:
        """Parse a selection set into individual fields"""
        fields = []

        # Split by top-level commas (not inside nested braces or parentheses)
        field_strings = self._split_selection_set(selection_set)

        for field_string in field_strings:
            field = self._parse_single_field(field_string.strip())
            if field:
                fields.append(field)

        return fields

    def _split_selection_set(self, selection_set: str) -> list[str]:
        """Split selection set by top-level commas"""
        fields = []
        current_field = ""
        paren_count = 0
        brace_count = 0

        for char in selection_set:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            elif char == ',' and paren_count == 0 and brace_count == 0:
                if current_field.strip():
                    fields.append(current_field.strip())
                current_field = ""
                continue

            current_field += char

        if current_field.strip():
            fields.append(current_field.strip())

        return fields

    def _parse_single_field(self, field_string: str) -> QueryField | None:
        """Parse a single field string"""
        if not field_string:
            return None

        # Parse field name and alias
        field_match = re.match(r'^(?:(\w+):\s*)?(\w+)', field_string)
        if not field_match:
            return None

        alias = field_match.group(1)
        field_name = field_match.group(2)

        # Parse arguments
        arguments = self._parse_arguments(field_string)

        # Parse directives
        directives = self._parse_directives(field_string)

        # Parse nested selections
        selections = []
        brace_start = field_string.find('{')
        if brace_start != -1:
            # Find matching closing brace
            brace_count = 0
            end_pos = brace_start

            for i, char in enumerate(field_string[brace_start:], brace_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break

            nested_selection = field_string[brace_start + 1:end_pos]
            selections = self._parse_selection_set(nested_selection)

        return QueryField(
            name=field_name,
            alias=alias,
            arguments=arguments,
            directives=directives,
            selections=selections
        )

    def _parse_arguments(self, field_string: str) -> dict[str, Any]:
        """Parse arguments from field string"""
        arguments = {}

        # Find arguments in parentheses
        arg_match = re.search(r'\(([^)]+)\)', field_string)
        if arg_match:
            arg_string = arg_match.group(1)

            # Parse individual arguments
            arg_pairs = self._split_arguments(arg_string)
            for arg_pair in arg_pairs:
                key_value = arg_pair.split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = self._parse_argument_value(key_value[1].strip())
                    arguments[key] = value

        return arguments

    def _split_arguments(self, arg_string: str) -> list[str]:
        """Split argument string by commas"""
        args = []
        current_arg = ""
        paren_count = 0
        bracket_count = 0

        for char in arg_string:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            elif char == ',' and paren_count == 0 and bracket_count == 0:
                if current_arg.strip():
                    args.append(current_arg.strip())
                current_arg = ""
                continue

            current_arg += char

        if current_arg.strip():
            args.append(current_arg.strip())

        return args

    def _parse_argument_value(self, value_string: str) -> Any:
        """Parse argument value"""
        value_string = value_string.strip()

        # Remove quotes for strings
        if value_string.startswith('"') and value_string.endswith('"'):
            return value_string[1:-1]

        # Parse numbers
        try:
            if '.' in value_string:
                return float(value_string)
            else:
                return int(value_string)
        except ValueError:
            pass

        # Parse booleans
        if value_string.lower() == 'true':
            return True
        elif value_string.lower() == 'false':
            return False

        # Parse arrays
        if value_string.startswith('[') and value_string.endswith(']'):
            array_content = value_string[1:-1]
            if array_content:
                elements = [self._parse_argument_value(elem.strip())
                           for elem in array_content.split(',')]
                return elements
            return []

        # Return as string if can't parse
        return value_string

    def _parse_directives(self, field_string: str) -> list[dict[str, Any]]:
        """Parse directives from field string"""
        directives = []

        # Find all directives
        directive_matches = re.finditer(r'@(\w+)(?:\(([^)]+)\))?', field_string)

        for match in directive_matches:
            directive_name = match.group(1)
            directive_args = {}

            if match.group(2):
                arg_string = match.group(2)
                arg_pairs = self._split_arguments(arg_string)
                for arg_pair in arg_pairs:
                    key_value = arg_pair.split(':', 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = self._parse_argument_value(key_value[1].strip())
                        directive_args[key] = value

            directives.append({
                "name": directive_name,
                "arguments": directive_args
            })

        return directives

    def _generate_query_embedding(self, parsed_query: ParsedQuery) -> np.ndarray:
        """Generate embedding for parsed query"""
        embedding = np.zeros(self.embedding_dim)

        # Operation type embedding
        op_type_embedding = {
            QueryType.QUERY: [1, 0, 0],
            QueryType.MUTATION: [0, 1, 0],
            QueryType.SUBSCRIPTION: [0, 0, 1]
        }

        op_embedding = op_type_embedding[parsed_query.operation_type]
        embedding[:3] = op_embedding

        # Field type embeddings
        field_embedding = np.zeros(4)
        for field in parsed_query.fields:
            if field.name in self.field_type_embeddings:
                field_embedding += self.field_type_embeddings[field.name]

        # Normalize field embeddings
        if np.linalg.norm(field_embedding) > 0:
            field_embedding = field_embedding / np.linalg.norm(field_embedding)

        embedding[3:7] = field_embedding

        # Add positional encoding for remaining dimensions
        for i in range(7, self.embedding_dim):
            pos = i - 7
            embedding[i] = np.sin(pos / (10000 ** (2 * (i % 10) / 10))) * 0.1

        return embedding

    def _build_graph_structure(self, parsed_query: ParsedQuery) -> tuple[list[dict], list[dict]]:
        """Build nodes and edges from parsed query"""
        nodes = []
        edges = []
        node_id_counter = 0
        edge_id_counter = 0

        # Create root node for operation
        root_node = {
            "id": f"node_{node_id_counter}",
            "type": "operation",
            "name": parsed_query.operation_type.value,
            "embedding": self._generate_node_embedding("operation", parsed_query.operation_type.value),
            "coordinates": (3, 3, 3),  # Center of 7x7x7 space
            "attention_score": 1.0,
            "layer": 0
        }
        nodes.append(root_node)
        node_id_counter += 1

        # Add field nodes and edges
        for field in parsed_query.fields:
            field_nodes, field_edges, node_id_counter, edge_id_counter = self._process_field(
                field, root_node["id"], node_id_counter, edge_id_counter, depth=1
            )
            nodes.extend(field_nodes)
            edges.extend(field_edges)

        return nodes, edges

    def _process_field(self, field: QueryField, parent_id: str,
                      node_id_counter: int, edge_id_counter: int,
                      depth: int) -> tuple[list[dict], list[dict], int, int]:
        """Process a single field and its selections"""
        nodes = []
        edges = []

        # Generate coordinates for this field
        coordinates = self._generate_field_coordinates(field.name, depth)

        # Create field node
        field_node = {
            "id": f"node_{node_id_counter}",
            "type": "field",
            "name": field.name,
            "alias": field.alias,
            "arguments": field.arguments,
            "directives": field.directives,
            "embedding": self._generate_node_embedding("field", field.name),
            "coordinates": coordinates,
            "attention_score": self._compute_field_attention(field),
            "layer": depth
        }
        nodes.append(field_node)
        field_node_id = field_node["id"]
        node_id_counter += 1

        # Create edge from parent to this field
        edge = {
            "id": f"edge_{edge_id_counter}",
            "source": parent_id,
            "target": field_node_id,
            "weight": 1.0,
            "type": "parent_child",
            "message_vector": np.zeros(self.embedding_dim).tolist(),
            "attention_weight": 1.0
        }
        edges.append(edge)
        edge_id_counter += 1

        # Process nested selections
        for selection in field.selections:
            sel_nodes, sel_edges, node_id_counter, edge_id_counter = self._process_field(
                selection, field_node_id, node_id_counter, edge_id_counter, depth + 1
            )
            nodes.extend(sel_nodes)
            edges.extend(sel_edges)

        return nodes, edges, node_id_counter, edge_id_counter

    def _generate_node_embedding(self, node_type: str, name: str) -> list[float]:
        """Generate embedding for a graph node"""
        embedding = np.zeros(self.embedding_dim)

        # Type-based encoding
        type_encodings = {
            "operation": [1, 0, 0, 0],
            "field": [0, 1, 0, 0],
            "argument": [0, 0, 1, 0],
            "directive": [0, 0, 0, 1]
        }

        if node_type in type_encodings:
            embedding[:4] = type_encodings[node_type]

        # Name-based encoding (simple hash)
        name_hash = hash(name) % 1000
        embedding[4] = name_hash / 1000.0

        # Fill remaining dimensions with positional encoding
        for i in range(5, self.embedding_dim):
            pos = i - 5
            embedding[i] = np.sin(pos / (10000 ** (2 * (i % 10) / 10))) * 0.1

        return embedding.tolist()

    def _generate_field_coordinates(self, field_name: str, depth: int) -> tuple[int, int, int]:
        """Generate 3D coordinates for field within 7x7x7 space"""
        # Hash field name to get base coordinates
        name_hash = hash(field_name)

        x = (name_hash % 7)
        y = ((name_hash // 7) % 7)
        z = min(depth, 6)  # Depth becomes z-coordinate, clamped to 6

        return (x, y, z)

    def _compute_field_attention(self, field: QueryField) -> float:
        """Compute attention score for a field"""
        base_attention = 0.5

        # Higher attention for fields with directives
        if field.directives:
            base_attention += 0.2 * len(field.directives)

        # Higher attention for fields with arguments
        if field.arguments:
            base_attention += 0.1 * len(field.arguments)

        # Higher attention for fields with selections
        if field.selections:
            base_attention += 0.1 * len(field.selections)

        return min(1.0, base_attention)

    def _compute_attention_weights(self, parsed_query: ParsedQuery,
                                  nodes: list[dict]) -> np.ndarray:
        """Compute attention weight matrix"""
        attention_matrix = np.zeros((7, 7))

        # Aggregate attention scores by x,y coordinates
        coord_attention = {}
        for node in nodes:
            x, y, _z = node["coordinates"]
            key = (x, y)

            if key not in coord_attention:
                coord_attention[key] = []
            coord_attention[key].append(node["attention_score"])

        # Fill attention matrix
        for (x, y), scores in coord_attention.items():
            if x < 7 and y < 7:
                attention_matrix[x, y] = np.mean(scores)

        return attention_matrix


def main():
    """Test the GraphQL query parser"""
    print("=== GraphQL Query Parser Test ===")

    # Create parser
    parser = GraphQLQueryParser()

    # Test queries
    test_queries = [
        """
        query TestQuery($nodeId: ID!) {
            getNeuralGraph(id: $nodeId) {
                nodes {
                    id
                    embedding
                    attention_score
                }
                edges {
                    source
                    target
                    weight
                }
            }
            getAttentionState(layer: 3, head: 4) @neural_attention(head: 4, weight: 0.8) {
                attention_weights
            }
        }
        """,
        """
        mutation UpdateWeights {
            updateNeuralWeights(
                graph_id: "graph_1"
                weights: [0.1, 0.2, 0.3]
            ) @message_passing(layers: 7, aggregation: "mean") {
                tensor_shape
                current_state
            }
        }
        """,
        """
        subscription AttentionFlow {
            attentionUpdates(graph_id: "graph_1") {
                head_id
                attention_weights
            }
        }
        """
    ]

    for i, query in enumerate(test_queries):
        print(f"\n--- Test Query {i + 1} ---")
        print(f"Query: {query.strip()}")

        # Parse query
        parsed = parser.parse_query(query)
        print(f"Operation: {parsed.operation_type.value}")
        print(f"Fields: {[f.name for f in parsed.fields]}")

        # Convert to neural graph
        neural_graph = parser.query_to_neural_graph(parsed)
        print(f"Nodes: {len(neural_graph.nodes)}")
        print(f"Edges: {len(neural_graph.edges)}")
        print(f"Query embedding shape: {neural_graph.query_embedding.shape}")
        print(f"Attention matrix shape: {neural_graph.attention_weights.shape}")

        # Save detailed results for first query
        if i == 0:
            result = {
                "parsed_query": {
                    "operation_type": parsed.operation_type.value,
                    "operation_name": parsed.operation_name,
                    "variables": parsed.variables,
                    "fields": [asdict(f) for f in parsed.fields]
                },
                "neural_graph": {
                    "nodes": neural_graph.nodes,
                    "edges": neural_graph.edges,
                    "tensor_shape": neural_graph.tensor_shape,
                    "query_embedding": neural_graph.query_embedding.tolist(),
                    "attention_weights": neural_graph.attention_weights.tolist()
                }
            }

            with open("query_parser_results.json", "w") as f:
                json.dump(result, f, indent=2)

            print("Detailed results saved to query_parser_results.json")

    print("\n=== GraphQL Query Parser Test Complete ===")


if __name__ == "__main__":
    main()
