# graph represents edges between nodes in a map
class Graph:
    # constructor - empty dictionaries
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    # add a node to the graph
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # add a directed edge to the graph
    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights.update({(from_vertex, to_vertex): weight})
        self.adjacency_list[from_vertex].append(to_vertex)

    # add an undirected edge to the graph
    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)
