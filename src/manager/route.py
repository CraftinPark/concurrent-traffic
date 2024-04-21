from __future__ import annotations # this enables Node from using declarations of Edge that come afterward

class Node():
    position: list = None
    in_edges: list[Edge] = []
    out_edges: list[Edge] = []

    def __init__(self, position: list):
        self.position = position

    def add_in_edge(self, edge: Edge):
        self.in_edges.append(edge)

    def add_out_edge(self, edge: Edge):
        self.out_edges.append(edge)

class Edge():
    start: Node = None
    end: Node = None
    straight: bool = True
    center = None # center is only required for curved edges

    def __init__(self, start: Node, end: Node, straight:bool=True, center=None):
        self.start = start
        self.end = end
        self.straight = straight
        if self.straight == False and center == None:
            raise ValueError("center point must be provided if edge is not straight")
        self.center = center

class Route():
    edges: list[Edge] = []
    def __init__(self, edges: list[Edge]):
        self.edges = edges