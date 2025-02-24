from graph import Graph

POSSIBLE_COLORS = ['green', 'red', 'blue']

class CSP:
    """Base class for a Constraint Satisfaction Problem """
    def __init__(self, aMap):
        self.mapAsGraph = Graph(aMap)  # Convert adjacency list to a graph
        self.variables = list(self.mapAsGraph.graph.keys())  # Regions (Nodes)
        self.domains = {region: POSSIBLE_COLORS[:] for region in self.variables}  # Colors for each region
        self.assignment = {}  # Stores the final colors assigned to each region 

    def is_valid_assignment(self, region, color):
        """Check if assigning `color` to `region` is valid (neighbors must have different colors)."""
        for neighbor in self.mapAsGraph.graph[region]:
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False  # Conflict with neighbor
        return True

    def backtrack(self):
        """Recursive backtracking algorithm to solve the CSP"""
        if len(self.assignment) == len(self.variables):
            return self.assignment  # Solution found
        
        # Select an unassigned variable (MRV heuristic can be added here)
        region = [v for v in self.variables if v not in self.assignment][0]

        for color in self.domains[region]:
            if self.is_valid_assignment(region, color):
                self.assignment[region] = color  
                result = self.backtrack()  # recur to assign the next region
                if result:
                    return result  # Solution found
                del self.assignment[region]  # backtrack if dead end
        
        return None  # No solution found

    def solve(self):
        """wrapper to start backtracking search."""
        return self.backtrack()


# Example usage
australia = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'V': ['NSW'],
    'T': []    
}

csp = CSP(australia)
solution = csp.solve()
print("\nSolution (Coloring):", solution)