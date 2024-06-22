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
        print('Usage: python3 src/main.py <absolute_path_to_preset>')
        return
    
    nodes = []
    edges = []
    routes = []
    vehicles = []
    
    preset_name = sys.argv[1]
    manager = load_preset(preset_name, nodes, edges, routes, vehicles)
    run_simulation(vehicles, nodes, edges, routes, manager)

# appends nodes, edges, routes, and vehicles and returns manager with the given position and radius 
def load_preset(file_path, nodes, edges, routes, vehicles):
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

    manager_data = presets["manager"]
    manager = Manager(np.array([manager_data["position"][0],manager_data["position"][1]]), manager_data["radius"])

    return manager

if __name__ == "__main__":
    main()