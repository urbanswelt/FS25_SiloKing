import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# Path to the comparison summary file
input_file = "Giants/data/vehicles/comparison_summary.txt"
output_image = "Giants/data/vehicles/change_tree_structure.png"

# Parse summary file
file_changes = defaultdict(list)
with open(input_file, "r") as file:
    current_file = None
    for line in file:
        line = line.strip()
        if line.startswith("Changes detected in:"):
            current_file = line.split(":")[1].strip()
        elif current_file and line:
            file_changes[current_file].append(line)

# Build the graph
graph = nx.DiGraph()
for file, changes in file_changes.items():
    graph.add_node(file)
    for change in changes:
        graph.add_edge(file, change)

# Plot the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(graph, k=0.3, iterations=50)
nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=10, font_weight="bold")
plt.title("Tree Structure of Changes", fontsize=14)
plt.savefig(output_image)
plt.show()
