"""
This script visualizes knowledge graphs from JSON data.
It loads entity and relation data, creates a directed graph,
and generates a visual representation of the knowledge graph.
The script uses NetworkX for graph creation and Matplotlib for visualization.
Graphs are saved as PNG files in the './kgs' directory.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
from pydantic import BaseModel

def load_json_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def create_knowledge_graph(entities: List[str], relations: List[List[str]]) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from(entities)
    G.add_edges_from([(s, o, {'label': p}) for s, p, o in relations])
    return G

def visualize_knowledge_graph(G: nx.DiGraph, title: str) -> None:
    plt.figure(figsize=(60, 45))  # Increased figure size for more space
    pos = nx.spring_layout(G, k=10, iterations=1000)  # Increased k and iterations for more spread
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=8000)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Draw edges with arrows
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=30, 
                           connectionstyle="arc3,rad=0.3", width=1.5, arrowstyle='->',
                           min_source_margin=30, min_target_margin=30)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.title(title, fontsize=20)
    plt.axis('off')
    
    # Add more padding around the graph
    x_values, y_values = zip(*pos.values())
    x_margin = (max(x_values) - min(x_values)) * 0.4
    y_margin = (max(y_values) - min(y_values)) * 0.4
    plt.xlim(min(x_values) - x_margin, max(x_values) + x_margin)
    plt.ylim(min(y_values) - y_margin, max(y_values) + y_margin)
    
    plt.savefig(f"./kgs/{title.replace(' ', '_')}.png", dpi=300, bbox_inches='tight')
    plt.close()

def process_json_data(data: dict, filename: str) -> None:
    # Check if 'entities' key exists in the data
    if 'entities' not in data:
        raise KeyError("The 'entities' key is missing from the JSON data")
    
    # Knowledge Graph
    G = create_knowledge_graph(data['entities'], data['relations'])
    visualize_knowledge_graph(G, filename)

def main():
    json_files = [
        # "harmless_base_chosen_test_50.jsonl",
        # "harmless_base_rejected_test_50.jsonl"
        "advil.json"
    ]
    
    for filename in json_files:
        try:
            json_data = load_json_data(f'./kgs/{filename}')
            process_json_data(json_data, filename)
            print(f"Successfully processed {filename}")
        except KeyError as e:
            print(f"Error processing {filename}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {filename}: {e}")

if __name__ == "__main__":
    main()
