import sys
sys.path.append(sys.path[0]+"/classes")
sys.path.append(sys.path[0]+"/manager")
sys.path.append(sys.path[0]+"/simulator")
from vehicle import Vehicle
from simulator import run_simulation

def main():
    # evenutually, we will load a preset as an argument and supply it to run_simulation
    # intialize_world()?

    # for now, supply a preset here
    vehicles = []
    vehicles.append(Vehicle([-50,1.5],[15,0],[0,0],[1,0],1.95,4.90))
    vehicles.append(Vehicle([-1.5,-50],[0,15],[0,0],[0,1],1.95,4.90))
    vehicles.append(Vehicle([1.5,50],[0,-15],[0,0],[0,-1],1.95,4.90))

    run_simulation(initial_vehicles=vehicles)

if __name__ == "__main__":
    main()