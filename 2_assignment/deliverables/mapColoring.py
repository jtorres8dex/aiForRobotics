from graph import Graph

POSSIBLE_COLORS = ['green', 'red', 'blue']

class ConstraintSatisfactionProblem:
    def __init__(self, aMap):
        self.mapAsGraph = Graph(aMap)  
        self.variables = list(self.mapAsGraph.graph.keys())  # regions (Nodes)
        self.domains = {region: POSSIBLE_COLORS[:] for region in self.variables}  # colors for each region
        self.assignment = {}  
        print(self.mapAsGraph)  

    def is_valid_assignment(self, region, color):
        """Check if assigning color to region is valid (neighbors must have different colors)."""
        for neighbor in self.mapAsGraph.graph[region]:
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False  # Conflict with neighbor
        return True

    def backtrack(self):
        """Recursive backtracking algo"""
        if len(self.assignment) == len(self.variables):
            return self.assignment  # Solution found
        
        region = [v for v in self.variables if v not in self.assignment][0]

        for color in self.domains[region]:
            if self.is_valid_assignment(region, color):
                self.assignment[region] = color  # Assign color
                result = self.backtrack()  # recur to assign the next region
                if result:
                    return result  # Solution found
                del self.assignment[region]  # backtrack
        
        return None  # No solution found

    def solve(self):
        """wrapper to backtracking search"""
        return self.backtrack()


# Example 
australia = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'V': ['NSW'],
    'T': []    
}

variables = list(australia.keys())
domains = {region: POSSIBLE_COLORS[:] for region in variables} 

csp = ConstraintSatisfactionProblem(australia)
solution = csp.solve()
print("\nSolution (Coloring):", solution)

import networkx as nx
import matplotlib.pyplot as plt

def visualize_coloring(graph, solution):
    """Visualize the colored map using NetworkX."""
    G = nx.Graph()

    for region in graph.keys():
        G.add_node(region, color=solution[region])

    for region, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(region, neighbor)

    node_colors = [solution[node] for node in G.nodes]

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="black", node_size=3000, font_size=12, font_weight="bold")
    plt.title("Map Coloring Solution")
    plt.show()

# AUSTRAIIA    
visualize_coloring(australia, solution)

# MAP GIVEN IN GITHUB EXAMPLE
POSSIBLE_COLORS = ['green', 'red', 'blue', 'yellow', 'purple', 'orange']
cmap = {}
variables = list(cmap.keys())
domains = {region: POSSIBLE_COLORS[:] for region in variables} 
cmap["ab"] = ["bc","nt","sk"]
cmap["bc"] = ["yt", "nt", "ab"]
cmap["mb"] = ["sk","nu","on"]
cmap["nb"] = ["qc", "ns", "pe"]
cmap["ns"] = ["nb", "pe"]
cmap["nl"] = ["qc"]
cmap["nt"] = ["bc", "yt", "ab", "sk", "nu"]
cmap["nu"] = ["nt", "mb"]
cmap["on"] = ["mb", "qc"]
cmap["pe"] = ["nb", "ns"]
cmap["qc"] = ["on", "nb", "nl"]
cmap["sk"] = ["ab", "mb", "nt"]
cmap["yt"] = ["bc", "nt"]

csp = ConstraintSatisfactionProblem(cmap)
solution = csp.solve()
print("\nSolution (Coloring):", solution)

visualize_coloring(cmap, solution)