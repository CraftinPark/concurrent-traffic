import numpy as np
from classes.vehicle import Vehicle
from manager.manager import Manager
from classes.node import Node
from classes.edge import StraightEdge, CircularEdge
from classes.route import Route
from simulator.simulator import run_simulation
from helper import get_intersections

def main():
    # evenutually, we will load a preset as an argument and supply it to run_simulation
    # intialize_world()?

    # for now, supply a preset here

    nodes = []
    edges = []
    routes = []
    vehicles = []

    # before intersection
    nodes.append(Node(np.array([-1.5,   80]))) # south
    nodes.append(Node(np.array([ 1.5,   80])))
    nodes.append(Node(np.array([  80,  1.5]))) # east
    nodes.append(Node(np.array([  80, -1.5])))
    nodes.append(Node(np.array([ 1.5,  -80]))) # north
    nodes.append(Node(np.array([-1.5,  -80])))
    nodes.append(Node(np.array([ -80, -1.5]))) # west
    nodes.append(Node(np.array([ -80,  1.5])))

    # at intersection
    nodes.append(Node(np.array([-1.5,    6]))) # south   r5 end
    nodes.append(Node(np.array([ 1.5,    6])))
    nodes.append(Node(np.array([   6,  1.5]))) # east
    nodes.append(Node(np.array([   6, -1.5]))) #r5 start
    nodes.append(Node(np.array([ 1.5,   -6]))) # north
    nodes.append(Node(np.array([-1.5,   -6])))
    nodes.append(Node(np.array([  -6, -1.5]))) # west
    nodes.append(Node(np.array([  -6,  1.5])))

    # edges outside intersection
    edges.append(StraightEdge(nodes[ 8], nodes[ 0]))
    edges.append(StraightEdge(nodes[ 1], nodes[ 9]))
    edges.append(StraightEdge(nodes[10], nodes[ 2]))
    edges.append(StraightEdge(nodes[ 3], nodes[11]))
    edges.append(StraightEdge(nodes[12], nodes[ 4]))
    edges.append(StraightEdge(nodes[ 5], nodes[13]))
    edges.append(StraightEdge(nodes[14], nodes[ 6]))
    edges.append(StraightEdge(nodes[ 7], nodes[15])) # far left to left of intersection

    # edges within intersection
    edges.append(StraightEdge(nodes[ 9], nodes[12])) # straight from south
    edges.append(CircularEdge(nodes[ 9], nodes[10], center=np.array([ 6, 6]), clockwise=True)) # right from south
    edges.append(CircularEdge(nodes[ 9], nodes[14], center=np.array([-6, 6]), clockwise=False)) # left from south

    edges.append(StraightEdge(nodes[11], nodes[14])) # straight from east
    edges.append(CircularEdge(nodes[11], nodes[12], center=np.array([ 6,-6]), clockwise=True)) # right from east
    edges.append(CircularEdge(nodes[11], nodes[ 8], center=np.array([ 6, 6]), clockwise=False)) # left from east

    edges.append(StraightEdge(nodes[13], nodes[ 8])) # straight from north
    edges.append(CircularEdge(nodes[13], nodes[14], center=np.array([-6,-6]), clockwise=True)) # right from north
    edges.append(CircularEdge(nodes[13], nodes[10], center=np.array([ 6,-6]), clockwise=False)) # left from north
    
    edges.append(StraightEdge(nodes[15], nodes[10])) # straight from west
    edges.append(CircularEdge(nodes[15], nodes[ 8], center=np.array([-6, 6]), clockwise=True)) # right from west
    edges.append(CircularEdge(nodes[15], nodes[12], center=np.array([-6,-6]), clockwise=False)) # left from west

    # routes
    routes.append(Route(0,  [edges[ 1], edges[ 8], edges[ 4]])) # straight from south
    routes.append(Route(1,  [edges[ 1], edges[ 9], edges[ 2]])) # right from south
    routes.append(Route(2,  [edges[ 1], edges[10], edges[ 6]])) # left from south

    routes.append(Route(3,  [edges[ 3], edges[11], edges[ 6]])) # straight from east
    routes.append(Route(4,  [edges[ 3], edges[12], edges[ 4]])) # right from east
    routes.append(Route(5,  [edges[ 3], edges[13], edges[ 0]])) # left from east

    routes.append(Route(6,  [edges[ 5], edges[14], edges[ 0]])) # straight from north
    routes.append(Route(7,  [edges[ 5], edges[15], edges[ 6]])) # right from north
    routes.append(Route(8,  [edges[ 5], edges[16], edges[ 2]])) # left from north

    routes.append(Route(9,  [edges[ 7], edges[17], edges[ 2]])) # straight from west
    routes.append(Route(10, [edges[ 7], edges[18], edges[ 0]])) # right from west
    routes.append(Route(11, [edges[ 7], edges[19], edges[ 4]])) # left from west

    vehicles.append(Vehicle(0,routes[0],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # south to north
    vehicles.append(Vehicle(1,routes[1],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # south to east
    vehicles.append(Vehicle(2,routes[2],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # south to west

    vehicles.append(Vehicle(3,routes[3],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # east to west
    vehicles.append(Vehicle(4,routes[4],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # east to north
    vehicles.append(Vehicle(5,routes[5],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # east to south

    vehicles.append(Vehicle(6,routes[6],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # north to south
    vehicles.append(Vehicle(7,routes[7],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # north to west
    vehicles.append(Vehicle(8,routes[8],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # north to east

    vehicles.append(Vehicle(9,routes[9],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # west to east
    vehicles.append(Vehicle(10,routes[10],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # west to south
    vehicles.append(Vehicle(11,routes[11],0,8,0,2.23,4.90,1.25,'assets/sedan.png')) # west to north

    manager = Manager(np.array([0,0]), 50, routes)

    # scenery
    # 2 rects for road,
    intersection_points = get_intersections(routes)
    run_simulation(vehicles, nodes, edges, routes, intersection_points, manager)

if __name__ == "__main__":
    main()