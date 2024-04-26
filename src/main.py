import sys
sys.path.append(sys.path[0]+"/classes")
sys.path.append(sys.path[0]+"/manager")
sys.path.append(sys.path[0]+"/simulator")
from vehicle import Vehicle
from route import Node, Edge, Route
from simulator import run_simulation

def main():
    # evenutually, we will load a preset as an argument and supply it to run_simulation
    # intialize_world()?

    # for now, supply a preset here

    nodes = []
    edges = []
    routes = []
    vehicles = []

    # before intersection
    nodes.append(Node([-1.5,   50])) # south
    nodes.append(Node([ 1.5,   50]))
    nodes.append(Node([  50,  1.5])) # east
    nodes.append(Node([  50, -1.5]))
    nodes.append(Node([ 1.5,  -50])) # north
    nodes.append(Node([-1.5,  -50]))
    nodes.append(Node([ -50, -1.5])) # west
    nodes.append(Node([ -50,  1.5]))

    # at intersection
    nodes.append(Node([-1.5,    6])) # south
    nodes.append(Node([ 1.5,    6]))
    nodes.append(Node([   6,  1.5])) # east
    nodes.append(Node([   6, -1.5]))
    nodes.append(Node([ 1.5,   -6])) # north
    nodes.append(Node([-1.5,   -6]))
    nodes.append(Node([  -6, -1.5])) # west
    nodes.append(Node([  -6,  1.5]))

    # edges before intersection
    edges.append(Edge(nodes[ 0], nodes[ 8]))
    edges.append(Edge(nodes[ 1], nodes[ 9]))
    edges.append(Edge(nodes[ 2], nodes[10]))
    edges.append(Edge(nodes[ 3], nodes[11]))
    edges.append(Edge(nodes[ 4], nodes[12]))
    edges.append(Edge(nodes[ 5], nodes[13]))
    edges.append(Edge(nodes[ 6], nodes[14]))
    edges.append(Edge(nodes[ 7], nodes[15]))

    # edges within intersection
    edges.append(Edge(nodes[ 9], nodes[12])) # straight from south
    edges.append(Edge(nodes[ 9], nodes[10], curved=True, center=[ 6, 6])) # right from south
    edges.append(Edge(nodes[ 9], nodes[14], curved=True, center=[-6, 6])) # left from south

    edges.append(Edge(nodes[11], nodes[14])) # straight from east
    edges.append(Edge(nodes[11], nodes[12], curved=True, center=[ 6,-6])) # right from east
    edges.append(Edge(nodes[11], nodes[ 8], curved=True, center=[ 6, 6])) # left from east

    edges.append(Edge(nodes[13], nodes[ 8])) # straight from north
    edges.append(Edge(nodes[13], nodes[14], curved=True, center=[-6,-6])) # right from north
    edges.append(Edge(nodes[13], nodes[10], curved=True, center=[ 6,-6])) # left from north

    edges.append(Edge(nodes[15], nodes[10])) # straight from west
    edges.append(Edge(nodes[15], nodes[ 8], curved=True, center=[-6, 6])) # right from west
    edges.append(Edge(nodes[15], nodes[12], curved=True, center=[-6,-6])) # left from west

    # routes
    routes.append(Route([edges[ 1], edges[ 8], edges[ 4]])) # straight from south
    routes.append(Route([edges[ 1], edges[ 9], edges[ 2]])) # right from south
    routes.append(Route([edges[ 1], edges[10], edges[ 6]])) # left from south

    routes.append(Route([edges[ 3], edges[11], edges[ 6]])) # straight from east
    routes.append(Route([edges[ 3], edges[12], edges[ 4]])) # right from east
    routes.append(Route([edges[ 3], edges[13], edges[ 8]])) # left from east

    routes.append(Route([edges[ 5], edges[14], edges[ 8]])) # straight from north
    routes.append(Route([edges[ 5], edges[15], edges[ 6]])) # right from north
    routes.append(Route([edges[ 5], edges[16], edges[10]])) # left from north

    routes.append(Route([edges[ 7], edges[17], edges[10]])) # straight from west
    routes.append(Route([edges[ 7], edges[18], edges[ 8]])) # right from west
    routes.append(Route([edges[ 7], edges[19], edges[12]])) # left from west

    vehicles.append(Vehicle([-50,1.5],[8,0],[0,0],[1,0],1.95,4.90, 'sedan.png'))  # west to east
    vehicles.append(Vehicle([-1.5,-50],[0,8],[0,0],[0,1],1.95,4.90, 'sedan.png')) # north to south
    vehicles.append(Vehicle([1.5,50],[0,-8],[0,0],[0,-1],1.95,4.90, 'sedan.png')) # south to north

    # scenery
    # 2 rects for road, 

    run_simulation(vehicles, nodes, edges, routes)

if __name__ == "__main__":
    main()