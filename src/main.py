import sys

from simulator.simulator import run_simulation
from helper import load_preset

def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 src/main.py <absolute_path_to_preset>')
        return
    
    preset_name = sys.argv[1]
    manager, nodes, curr_edges, routes, intersection_points, vehicles = load_preset(preset_name)

    run_simulation(vehicles, nodes, curr_edges, routes, intersection_points, manager)

if __name__ == "__main__":
    main()