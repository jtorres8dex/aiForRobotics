from graph import Graph, Node
from dataclasses import dataclass
"""
variables
domain 
constraints
"""



class State(Node):
    def __init__(self, color: str = None, neighbors: list[str] = []):
        self.color: str = color
        self.neighbors = neighbors
    def __eq__(self, other):
        return self.color == other.color        
    def _setColor(self, color: str):
        self.color = color
    def _getColor(self) -> str:
        return self.color


class ConstraintSatisfactionProblem(Graph):

    def __init__(self, domain: list[str]=[], map={}):
        super().__init__(map)
        self.domain = domain


POSSIBLE_COLORS = ['green', 'red', 'blue']
STATES = {'WA','NT','Q','NSW','V','SA','T'}

csp = ConstraintSatisfactionProblem(POSSIBLE_COLORS, STATES)


map = {
    'WA': ['NT','SA'],
    'NT': ['WA','SA','Q'],
    'SA': ['WA','NT','Q'],
    'Q': ['NT','SA','NSW'],
    'NSW': ['SA','Q','V'],
    'T': []    
}

class CSP:
    def __init__(self, vars, domains, constraints):
        self.variables = vars
        self.domains = domains 
        self.constraints = constraints
        self.assignment = {}

    def isConsistent(self, var, value) -> bool:
        """check if var can be value while still satisfying contraints"""
        for other_var, other_value in self.assignment.items():
            if (var, other_var) in self.constraints and not self.constraints[(var, other_var)](value, other_value):
                return False
        return True