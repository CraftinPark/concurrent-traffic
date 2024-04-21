import sys
sys.path.append(sys.path[0]+"/classes")
sys.path.append(sys.path[0]+"/manager")
sys.path.append(sys.path[0]+"/simulator")
from run_simulation import run_simulation

def main():
    # evenutually, we will load a preset as an argument and supply it to run_simulation
    # intialize_world()?
    run_simulation()

if __name__ == "__main__":
    main()