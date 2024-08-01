import sys
import numpy as np
import json

from manager.manager import Manager
from classes.node import Node
from classes.edge import Edge
from classes.route import Route
from classes.vehicle import Vehicle
from simulator.simulator import run_simulation
from helper import get_intersections, load_nodes, load_edges, load_routes, load_vehicles
import argparse

def main() -> None:
    verbose = False
    # Check if -v flag is present
    if '-v' in sys.argv:
        verbose = True
        sys.argv.remove('-v')
    
    if len(sys.argv) != 2:
        print('Usage: python3 src/main.py <absolute_path_to_preset>')
        return
    
    preset_name = sys.argv[1]
    if verbose:
        print(f"Logging is enabled for preset: {preset_name}")
    
    manager, nodes, curr_edges, routes, vehicles = load_preset(preset_name)
    intersection_points = get_intersections(routes)
    run_simulation(vehicles, nodes, curr_edges, routes, intersection_points, manager)
    
    if(verbose):
        print(manager.events)
        #TODO: gotta log in a file as well

def load_preset(file_path: str) -> tuple[Manager, list[Node], list[Edge], list[Route], list[Vehicle]]:
    with open(file_path, 'r') as file:
        presets = json.load(file)

    nodes, curr_edges, routes, vehicles = [], [], [], []
        
    node_dict = load_nodes(presets["nodes"], nodes)
    edge_dict = load_edges(presets['edges'], curr_edges, node_dict)
    route_dict = load_routes(presets['routes'], routes, edge_dict)
    load_vehicles(presets["stored_vehicles"], vehicles, route_dict)
    
    manager_data = presets["manager"]
    manager = Manager(np.array(manager_data["position"]), manager_data["radius"], routes)

    return manager, nodes, curr_edges, routes, vehicles

if __name__ == "__main__":
    main()