# class Node()
# position

# class Edge()
# edge must be defined as either straight, or curved. If curved, it needs to define the information required to interpolate the curve.


class Route():
    nodes = []
    edges = []
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges