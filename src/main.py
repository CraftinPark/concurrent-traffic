import sys
import numpy as np
import json
from classes.vehicle import Vehicle
from manager.manager import Manager
from classes.node import Node
from classes.edge import StraightEdge, CircularEdge
from classes.route import Route
from simulator.simulator import run_simulation
from helper import get_intersections

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 src/main.py <absolute_path_to_preset>')
        return
    
    preset_name = sys.argv[1]
    nodes, edges, routes, vehicles = [], [], [], []
    
    manager = load_preset(preset_name, nodes, edges, routes, vehicles)
    run_simulation(vehicles, nodes, edges, routes, manager)

def load_preset(file_path, nodes, edges, routes, vehicles):
    with open(file_path, 'r') as file:
        presets = json.load(file)
        
    node_dict = load_nodes(presets["nodes"], nodes)
    edge_dict = load_edges(presets['edges'], edges, node_dict)
    route_dict = load_routes(presets['routes'], routes, edge_dict)
    load_vehicles(presets["stored_vehicles"], vehicles, route_dict)
    
    manager_data = presets["manager"]
    manager = Manager(np.array(manager_data["position"]), manager_data["radius"])

    return manager

def load_nodes(loaded_nodes, nodes):
    node_dict = {}
    for node in loaded_nodes:
        if node["id"] in node_dict:
            raise ValueError(f"Duplicate node ID found: {node['id']}")
        new_node = Node(np.array(node["position"]))
        node_dict[node["id"]] = new_node
        nodes.append(new_node)
    return node_dict

def load_edges(loaded_edges, edges, node_dict):
    edge_dict = {}
    for edge in loaded_edges:
        if edge["id"] in edge_dict:
            raise ValueError(f"Duplicate edge ID found: {edge['id']}")
        if edge.get("curved"):
            new_edge = Edge(node_dict[edge["source"]], node_dict[edge["target"]], edge["curved"], np.array(edge["center"]), edge["clockwise"])
        else:
            new_edge = Edge(node_dict[edge["source"]], node_dict[edge["target"]])
        edge_dict[edge["id"]] = new_edge
        edges.append(new_edge)
    return edge_dict

def load_routes(loaded_routes, routes, edge_dict):
    route_dict = {}
    for route in loaded_routes:
        if route["id"] in route_dict:
            raise ValueError(f"Duplicate route ID found: {route['id']}")
        
        source_edge = edge_dict[route["source"]]
        intermediate_edge = edge_dict[route["intermediate"]]
        target_edge = edge_dict[route["target"]]

        if source_edge.end != intermediate_edge.start or intermediate_edge.end != target_edge.start:
            raise ValueError("Invalid Route")

        new_route = Route([source_edge, intermediate_edge, target_edge])
        route_dict[route["id"]] = new_route
        routes.append(new_route)
    return route_dict

def load_vehicles(loaded_vehicles, vehicles, route_dict):
    vehicle_dict = {}
    for v in loaded_vehicles:
        if v["id"] in vehicle_dict:
            raise ValueError(f"Duplicate vehicle ID found: {v['id']}")
        new_vehicle = Vehicle(v["id"], route_dict[v["route"]], v["route_position"], 8, 0, 2.23, 4.90, 1.25, 'assets/sedan.png')
        vehicle_dict[v["id"]] = new_vehicle
        vehicles.append(new_vehicle)

if __name__ == "__main__":
    main()
