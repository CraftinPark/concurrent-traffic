import numpy as np
from classes.route import Route
from classes.node import Node
from classes.edge import Edge, StraightEdge, CircularEdge
from classes.vehicle import Vehicle
from standard_traffic.traffic_light import TrafficLight, TrafficState
import sympy
from sympy import Point2D
from itertools import combinations

def get_intersections(routes: list[Route]) -> set[tuple[int, int, tuple[float, float]]]:
    """Return a set of intersections in the following form: (route1_id, route2_id, (x, y))."""
    intersections = set()
    for r1, r2 in combinations(routes, 2):
        for e1 in r1.edges:
            for e2 in r2.edges:
                if e1 is e2:
                    continue
                intersections.update(get_edge_intersections(r1, r2, e1, e2))
    return intersections

def get_edge_intersections(route1: Route, route2: Route, edge1: Edge, edge2: Edge) -> set[tuple[int, int, tuple[float, float]]]:
    """Return the intersections between two Edges."""
    intersections = set(sympy.intersection(edge1.sympy_obj, edge2.sympy_obj))
    if isinstance(edge1, CircularEdge):
        remove_false_circle_intersects(edge1, intersections)
    if isinstance(edge2, CircularEdge):
       remove_false_circle_intersects(edge2, intersections)

    result = set()

    for i in intersections:
        intersection = (route1.current_id, route2.current_id, (float(i.x), float(i.y)))
        result.add(intersection)

    return result

def remove_false_circle_intersects(edge: CircularEdge, intersections: list[Point2D]) -> None:
    """Removes false positives for arc intersects."""
    start_angle = np.arctan2(-(edge.start.position[1] - edge.center[1]), edge.start.position[0] - edge.center[0])
    end_angle = np.arctan2(-(edge.end.position[1] - edge.center[1]), edge.end.position[0] - edge.center[0])

    intersections_to_remove = set()

    for i in intersections:
        i_angle = np.arctan2(-(float(i.y) - edge.center[1]), float(i.x) - edge.center[0])
        if not is_angle_between(start_angle, end_angle, i_angle, edge.clockwise):
           intersections_to_remove.add(i)

    intersections.difference_update(intersections_to_remove)

def is_angle_between(start_angle: float, end_angle: float, i_angle: float, clockwise: bool) -> bool:
    """Return True if i_angle is between start_angle and end_angle."""
    if start_angle <= end_angle and not clockwise:
        return start_angle <= i_angle <= end_angle
    elif start_angle <= end_angle and clockwise:
        return i_angle <= start_angle or i_angle >= end_angle
    elif start_angle >= end_angle and clockwise:
        return end_angle <= i_angle <= start_angle
    elif start_angle >= end_angle and not clockwise:
        return i_angle <= end_angle or i_angle >= start_angle
    
def load_nodes(loaded_nodes: object, nodes: list[Node]) -> dict[str, Node]:
    """Return id -> Node dictionary from the loaded_nodes json object. Also populates nodes list."""
    node_dict = {}
    for node in loaded_nodes:
        if node["id"] in node_dict:
            raise ValueError(f"Duplicate node ID found: {node['id']}")
        new_node = Node(np.array(node["position"]))
        node_dict[node["id"]] = new_node
        nodes.append(new_node)
    return node_dict

def load_edges(loaded_edges: object, edges: list[Edge], node_dict: dict[str, Node]) -> dict[str, Edge]:
    """Return id -> Edge dictionary from the loaded_edges json object. Also populates edges list."""
    edge_dict = {}
    for edge in loaded_edges:
        if edge["id"] in edge_dict:
            raise ValueError(f"Duplicate edge ID found: {edge['id']}")
        if edge.get("center"):
            new_edge = CircularEdge(edge["id"], node_dict[edge["source"]], node_dict[edge["target"]], np.array(edge["center"]), edge["clockwise"])
        else:
            new_edge = StraightEdge(edge["id"], node_dict[edge["source"]], node_dict[edge["target"]])
        edge_dict[edge["id"]] = new_edge
        edges.append(new_edge)
    return edge_dict

def load_routes(loaded_routes: object, routes: list[Route], edge_dict: dict[str, Edge]) -> dict[str, Route]:
    """Return id -> Route dictionary from the loaded_routes json object. Also populates routes list."""
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

def load_vehicles(loaded_vehicles: object, vehicles: list[Vehicle], route_dict: dict[str, Vehicle]) -> dict[str, Vehicle]:
    """Return id -> Vehicle dictionary from the loaded_vehicle json object. Also populates vehicles list."""
    vehicle_dict = {}
    for v in loaded_vehicles:
        if v["id"] in vehicle_dict:
            raise ValueError(f"Duplicate vehicle ID found: {v['id']}")
        new_vehicle = Vehicle(v["id"], v["name"], route_dict[v["route"]], v["route_position"], v["velocity"], 0, 2.23, 4.90, 1.25, 'assets/sedan.png')
        vehicle_dict[v["id"]] = new_vehicle
        vehicles.append(new_vehicle)
    # return vehicle_dict

def load_traffic_lights(loaded_lights: object, traffic_types: list[tuple], traffic_lights: list[TrafficLight], node_dict: dict[str, Node]) -> tuple[dict[str, tuple], dict[str, TrafficLight]]:
    """Return id -> TrafficLight dictionary from the traffic_lights json object. Also populates traffic_lights list."""
    light_dict, type_dict = {}, {}
    for obj in loaded_lights:
        if obj.get("type"):
            if obj["type"] in type_dict:
                raise ValueError(f"Duplicate traffic type found: {obj['type']}")
            type = (obj["type"], obj["red_duration"], obj["yellow_duration"], obj["green_duration"], TrafficState[obj["initial_state"]])
            type_dict[obj["type"]] = type
            traffic_types.append(type)
        else:
            if obj["id"] in light_dict:
                raise ValueError(f"Duplicate traffic_light ID found: {obj['id']}")
            if obj["identifier"] not in type_dict:
                raise KeyError(f"Identifier '{obj['identifier']}' not found in type_dict")
            new_light = TrafficLight(obj["id"], node_dict[obj["node_position"]], obj["identifier"])
            light_dict[obj["id"]] = new_light
            # new_light.time_to_switch = list(itertools.accumulate(type_dict[obj["identifier"]][1:-1]))
            traffic_lights.append(new_light)
    return type_dict, light_dict
