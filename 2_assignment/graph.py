class Node:
    def __init__(self, val=None, neighbors=None):
        self.val = val
        self.neighbors = set(neighbors) if neighbors else set()
    
    def __eq__(self, other):
        return self.val == other.val
    
    def __str__(self):
        return f"Node {self.val} has {len(self.neighbors)} neighbors."
    
    def setVal(self, val):
        self.val = val
    
    def setNeighbors(self, neighbors):
        self.neighbors = set(neighbors)


class Graph:
    def __init__(self, graph={}):
        self.graph = {}

        
        all_nodes = set(graph.keys())  # Explicitly defined nodes
        for neighbors in graph.values():
            all_nodes.update(neighbors)  # Add neighbor nodes

        # Initialize graph with empty neighbor lists
        for node in all_nodes:
            self.graph[node] = set(graph.get(node, []))  # Ensure each node has a neighbor list

        self.numNodes = len(self.graph)
        self.nodeVals = sorted(self.graph.keys())  # Sort for consistent indexing

    def __eq__(self, other):
        """Equality of graph denoted as same size and topology"""
        if len(self.graph) != len(other.graph):
            return False
        for key in self.graph:
            if key not in other.graph or self.graph[key] != other.graph[key]:
                return False
        return True
    
    def __str__(self):
        """Print adjacency matrix"""
        adj = self.getAdjacencyMatrix()
        
        if not isinstance(adj, list):
            raise TypeError(f"ERROR: Expected adj to be a list, but got {type(adj)}")

        return "\n".join(" ".join(map(str, row)) for row in adj)

    def getAdjacencyMatrix(self) -> list[list[int]]:
        """Returns the adjacency matrix for the graph"""
        N = self.numNodes
        adj = [[0 for _ in range(N)] for _ in range(N)]  # Correctly initializes a 2D list
        node_index = {node: i for i, node in enumerate(self.nodeVals)}  # Maps nodes to indices

        for node, neighbors in self.graph.items():
            i = node_index[node]  # Get row index
            for neighbor in neighbors:

                j = node_index[neighbor]  # Get column index
                adj[i][j] = 1  # Mark adjacency
                adj[j][i] = 1  # Ensure symmetry for undirected graphs

        return adj
