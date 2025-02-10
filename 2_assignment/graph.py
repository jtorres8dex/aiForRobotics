import numpy as np 

class Node:
    def __init__(self, val=None, neighbors=set()):
        self.val = val
        self.neighbors = neighbors

class Graph:

    def __init__(self, graph={}):
        self.graph = {}
        self.numNodes = 0

        # if provided a graph in form of dict, populate it 
        if graph:
            for val, neighbors in graph.items():
                self.graph[val] = neighbors
                self.numNodes += 1


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
        adj = np.ndarray(shape=(len(self.graph.keys()),len(self.graph.keys())))
        adj = []
        for node, nieghbors in self.graph.items():
            adjNodes = [node].extend(nieghbors)
            adj.append(adjNodes)
        return adj
        
if __name__ == "__main__":

    g = {
        'pa': ['nj', 'oh', 'md', 'ny', 'de', 'wv'],
        'nj': ['pa', 'ny', 'de', 'md'],
        'md': ['pa', 'nj', 'wv']
    }


emptyGraph = Graph()

ex = Graph(g)
print(ex.getAdjacencyMatrix())