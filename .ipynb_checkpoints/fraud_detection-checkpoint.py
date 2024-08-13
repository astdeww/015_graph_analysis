import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def analyze_graph(transactions):
    G = nx.DiGraph()
    for sender, receiver, amount in transactions:
        G.add_edge(sender, receiver, weight=amount)
    
    # Calculate betweenness centrality
    betweenness = nx.betweenness_centrality(G, normalized=True)
    
    # Calculate mean and standard deviation of betweenness centrality
    mean_betweenness = np.mean(list(betweenness.values()))
    std_betweenness = np.std(list(betweenness.values()))
    threshold = mean_betweenness + 2 * std_betenness
    
    # Flag anomalies
    anomalies = {node: bc for node, bc in betweenness.items() if bc > threshold}
    
    # Detect potential fraud based on transaction amounts
    frauds = {}
    for node in G.nodes:
        in_edges = G.in_edges(node, data=True)
        out_edges = G.out_edges(node, data=True)
        total_in = sum(data['weight'] for _, _, data in in_edges)
        total_out = sum(data['weight'] for _, _, data in out_edges)
        if total_in > 2 * total_out:
            frauds[node] = (total_in, total_out)
    
    return betweenness, anomalies, frauds

def visualize_graph(G, betweenness, anomalies):
    node_size = [v * 1000 for v in betweenness.values()]
    node_color = ['red' if node in anomalies else 'lightblue' for node in G.nodes()]
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_color, arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
