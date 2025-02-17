import numpy as np 
# from pydantic import BaseModel, ConfigDict

class Node:
    def __init__(self, val=None, neighbors=set()):
        self.val = val
        self.neighbors = neighbors

    def __eq__(self, other):
        return self.val == other.val

    def __str__(self):
        return f"Node {self.val} has {len(self.neighbors)} neighbors."

    def __getstate__(self):
        pass
        

class Graph():

    def __init__(self, graph={}):
        self.numNodes: int = 0
        self.graph: dict[str, list] = {}

        # if provided a graph in form of dict, populate it 
        if graph:
            for val, neighbors in graph.items():
                self.graph[val] = neighbors                
        else:
            self.graph = {}
        print(self.graph)
        self.numNodes = len(self.graph)            

    def __eq__(self, other):
        """Equality of graph denoted as same size and topology"""
        if len(self.graph) != len(other.graph):
            return False
        for key in self.graph:
            if key not in other.graph or self.graph[key] != other.graph[key]:
                return False
        return True
    
    def __str__(self):
        """For now, just print adjacency matrix"""
        adj = self.getAdjacencyMatrix()
        _str = ""
        for row in adj:
            # _str += row
            # _str.append(row)
            for col in row:
                _str += (col)
            _str += "\n"
        return _str
    
    ### Node Methods ###
    def addNode(self, node: Node):
        if node.val in self.graph.keys():
            raise ValueError(f"Node {node.val} already exists in graph!")
        self.graph[node.val] = node.neighbors
        self.numNodes += 1

    def removeNode(self, val: any):
        if not val in self.graph.keys():
            raise ValueError(f"{val} is not in graph!")
        del self.graph[val]

    def setNode(self, val: any, neighbors: set):
        if val not in self.graph.keys():
            raise ValueError(f"Tried setting node {val} which DNE")
        self.graph[val] = neighbors

    ### Graph Methods ###
    def getAdjacencyMatrix(self) -> list[list]:
        """returns adjacency matrix, should be used with nodes of numeric values"""
        adj = [[]]
        N = self.numNodes
        for node, neighbors in self.graph.items():
            # adjNodes = [node].extend(nieghbors)
            adj.append(neighbors)
        return adj
        
if __name__ == "__main__":

    g = {
        'pa': ['nj', 'oh', 'md', 'ny', 'de', 'wv'],
        'nj': ['pa', 'ny', 'de', 'md'],
        'md': ['pa', 'nj', 'wv']
    }


emptyGraph = Graph()

ex = Graph(g)
print(ex)

