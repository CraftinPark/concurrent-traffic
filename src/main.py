import sys
import numpy as np
import json
from classes.vehicle import Vehicle
from manager.manager import Manager
from classes.node import Node
from classes.edge import Edge, StraightEdge, CircularEdge
from classes.route import Route
from simulator.simulator import run_simulation
from helper import get_intersections

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 src/main.py <absolute_path_to_preset>')
        return
    
    preset_name = sys.argv[1]
    nodes, curr_edges, routes, vehicles = [], [], [], []
    
    manager = load_preset(preset_name, nodes, curr_edges, routes, vehicles)
    intersection_points = get_intersections(routes)
    run_simulation(vehicles, nodes, curr_edges, routes, intersection_points, manager)

def load_preset(file_path, nodes, curr_edges, routes, vehicles):
    with open(file_path, 'r') as file:
        presets = json.load(file)

    node_dict = load_nodes(presets["nodes"], nodes)
    edge_dict = load_edges(presets['edges'], curr_edges, node_dict)
    route_dict = load_routes(presets['routes'], routes, edge_dict)
    load_vehicles(presets["stored_vehicles"], vehicles, route_dict)
    
    manager_data = presets["manager"]
    manager = Manager(np.array(manager_data["position"]), manager_data["radius"], routes)

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

def load_edges(loaded_edges, curr_edges, node_dict):
    edge_dict = {}
    for edge in loaded_edges:
        if edge["id"] in edge_dict:
            raise ValueError(f"Duplicate edge ID found: {edge['id']}")
        if edge.get("center"):
            new_edge = CircularEdge(edge["id"], node_dict[edge["source"]], node_dict[edge["target"]], np.array(edge["center"]), edge["clockwise"])
        else:
            new_edge = StraightEdge(edge["id"], node_dict[edge["source"]], node_dict[edge["target"]])
        edge_dict[edge["id"]] = new_edge
        curr_edges.append(new_edge)
    return edge_dict

def load_routes(loaded_routes, routes, edge_dict: dict[str, Edge]):
    route_dict = {}

    for route in loaded_routes:
        if route["id"] in route_dict:
            raise ValueError(f"Duplicate route ID found: {route['id']}")
        
        source_edge = edge_dict[route["source"]]
        target_edge = edge_dict[route["target"]]
        intermediate_edges = []
        for i, e in enumerate(route["intermediate"]):
            if route["intermediate"][i] is route["intermediate"][0]:
                if source_edge.end != edge_dict[e].start:
                    raise ValueError(f"Invalid Route: {route['d']} end of source edge ({source_edge.edge_id}) does not match start of {edge_dict[e].edge_id}")
                
            elif route["intermediate"][i] is route["intermediate"][-1]:
                if edge_dict[e].end != target_edge.start:
                    raise ValueError(f"Invalid Route: {route['id']} end of {edge_dict[e].edge_id} does not match start of target edge ({target_edge.edge_id})")
                
            else:
                if edge_dict[route["intermediate"][i - 1]].end != edge_dict[e].start:
                    raise ValueError(f"Invalid Route: {route['id']} end of {edge_dict[route['intermediate'][i - 1]].end} does not match start of ({edge_dict[e].edge_id})")
                
                elif edge_dict[e].end != edge_dict[route["intermediate"][i + 1]].start:
                    raise ValueError(f"Invalid Route: {route['id']} end of {edge_dict[route['intermediate'][e]].end} does not match start of ({edge_dict[i + 1].edge_id})")

            intermediate_edges.append(edge_dict[e])

        curr_edges = []
        curr_edges.append(source_edge)
        curr_edges.extend(intermediate_edges)
        curr_edges.append(target_edge)

        new_route = Route(route["id"], curr_edges)
        route_dict[route["id"]] = new_route
        routes.append(new_route)

    return route_dict

def load_vehicles(loaded_vehicles, vehicles, route_dict):
    vehicle_dict = {}
    for v in loaded_vehicles:
        if v["id"] in vehicle_dict:
            raise ValueError(f"Duplicate vehicle ID found: {v['id']}")
        new_vehicle = Vehicle(v["id"], route_dict[v["route"]], v["route_position"], 8, 0, 2.23, 4.90, 1.25, 'assets/sedan.png')
        if new_vehicle.route_position > new_vehicle.route.total_length:
            raise ValueError(f"Vehicle {v['id']} (that has been added to the system) initial route position exceeds route length")
        vehicle_dict[v["id"]] = new_vehicle
        vehicles.append(new_vehicle)
    

if __name__ == "__main__":
    main()
