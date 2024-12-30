import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render

# TSP Solver using Nearest Neighbor
def nearest_neighbor_tsp(locations, distances):
    n = len(locations)
    visited = [False] * n
    path = []
    cost = 0
    current = 0
    for _ in range(n):
        visited[current] = True
        path.append(current)
        next_city = min(
            [(distances[current][j], j) for j in range(n) if not visited[j]],
            default=(None, None)
        )[1]
        if next_city is None:
            break
        cost += distances[current][next_city]
        current = next_city
    cost += distances[current][0]  # Return to starting point
    path.append(0)
    return {'path': path, 'cost': cost}
def visualize_tsp(locations, distances, path):
    G = nx.DiGraph()  # Directed graph for visualizing the path

    # Add nodes
    for loc in locations:
        G.add_node(loc)

    # Add edges with weights
    for i in range(len(distances)):
        for j in range(len(distances[i])):
            if i != j:
                G.add_edge(locations[i], locations[j], weight=distances[i][j])

    # Highlight the optimal TSP path
    path_edges = [(locations[path[i]], locations[path[i + 1]]) for i in range(len(path) - 1)]
    path_edges.append((locations[path[-1]], locations[path[0]]))  # Close the loop

    pos = nx.circular_layout(G)  # Circular layout
    plt.figure(figsize=(8, 8))

    # Draw the full graph
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Highlight the TSP path
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", arrows=True, width=2)

    # Save the graph as a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    return image_base64
def tsp_solver(request):
    result = None
    graph_base64 = None

    if request.method == 'POST':
        # Input parsing
        locations = [loc.strip() for loc in request.POST.get('locations', '').split(',')]
        distances_input = [row.strip() for row in request.POST.get('distances', '').strip().splitlines()]
        distances = [list(map(int, row.split(','))) for row in distances_input]

        if len(locations) != len(distances):
            result = {'error': 'Number of locations and matrix size mismatch'}
        else:
            # Solve TSP
            tsp_result = nearest_neighbor_tsp(locations, distances)
            path_indices = tsp_result['path']
            tsp_result['path'] = [locations[i] for i in path_indices]

            # Generate graph
            graph_base64 = visualize_tsp(locations, distances, path_indices)
            result = tsp_result

    return render(request, 'tsp_solver/tsp_solver.html', {'result': result, 'graph_base64': graph_base64})
