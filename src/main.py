import sys
import numpy as np
import json
from classes.vehicle import Vehicle
from manager.manager import Manager
from classes.node import Node
from classes.edge import Edge
from classes.route import Route
from simulator.simulator import run_simulation

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 src/main.py <preset_file_name>')
        return
    
    preset_name = sys.argv[1]
    load_preset("presets/" + preset_name)

def load_preset(file_path):
    nodes = []
    edges = []
    routes = []
    vehicles = []

    with open(file_path, 'r') as file:
        presets = json.load(file)
        
    # Usage of HashMap to find Node with ID
    node_dict = {}
    loaded_nodes = presets["nodes"]
    for node in loaded_nodes:
        new_node = Node(np.array([node["position"][0], node["position"][1]]))
        node_dict[node["id"]] = new_node
        nodes.append(new_node)

    edge_dict = {}
    loaded_edges = presets['edges']
    for edge in loaded_edges:
        if edge.get("curved"):
            new_edge = Edge(node_dict[edge["source"]], node_dict[edge["target"]], edge["curved"], np.array([ edge["center"][0], edge["center"][1]]), edge["clockwise"])
        else:
            new_edge = Edge(node_dict[edge["source"]], node_dict[edge["target"]])
        edge_dict[edge["id"]] = new_edge
        edges.append(new_edge)

    route_dict = {}
    loaded_routes = presets['routes']
    for route in loaded_routes:
        new_route = Route([edge_dict[route["source"]], edge_dict[route["intermediate"]], edge_dict[route["target"]]])
        route_dict[route["id"]] = new_route
        routes.append(new_route)
        
    loaded_vehicles = presets["stored_vehicles"]
    for v in loaded_vehicles:
        vehicles.append(Vehicle(v["id"],route_dict[v["route"]],v["route_position"],8,0,2.23,4.90,1.25,'assets/sedan.png'))

    manager = Manager(np.array([0,0]), 50)

    run_simulation(vehicles, nodes, edges, routes, manager)

if __name__ == "__main__":
    main()