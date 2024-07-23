from classes.edge import Edge, change_state, get_state
from classes.node import Node
from classes.edge import TrafficState
from enum import Enum, auto

class TrafficState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

    def next(self):
        if self == TrafficState.RED:
            return TrafficState.GREEN
        elif self == TrafficState.GREEN:
            return TrafficState.YELLOW
        elif self == TrafficState.YELLOW:
            return TrafficState.RED
        
    def get_color(self) -> str:
        if self == TrafficState.RED:
            return "red"
        elif self == TrafficState.GREEN:
            return "green"
        elif self == TrafficState.YELLOW:
            return "yellow"

class TrafficLight:
    state: TrafficState
    time_in_state: int
    cycle_duration: int
    id: str
    edge: Edge
    node: Node
    identifier: str # eg horizontal, vertical, horizontal_left_turn
    time_to_switch: list[float]

    def __init__(self, id: str, edge: Edge, node_pos: Node, identifier: str) -> None:
        # if not isinstance(initial_state, TrafficState):
        #     raise ValueError("initial_state must be an instance of TrafficState")
        # self.state = initial_state
        self.id = id
        self.edge = edge
        self.node = node_pos
        self.type = identifier
        self.state = TrafficState.GREEN
        self.time_in_state = 0 # set later by traffic_master
        self.cycle_duration = 0 # set later by traffic_master
        self.time_to_switch = [] # set later by traffic_master

def next_state(traffic_light: TrafficLight):
    traffic_light.state = traffic_light.state.next()
    new_state = get_state(traffic_light)
    change_state(traffic_light.edge, new_state)
    reset_time_in_state(traffic_light)

def reset_time_in_state(traffic_light: TrafficLight):
    traffic_light.time_in_state = 0

def get_state(traffic_light: TrafficLight) -> TrafficState:
    return traffic_light.state

def set_state(traffic_light: TrafficLight, state: TrafficState):
    traffic_light.state = state
    change_state(traffic_light.edge, state)

def set_cycle_dur(traffic_light: TrafficLight, duration: int):
    if duration < 1:
        raise ValueError(f"Cycle duration cannot be less than 1.")
    traffic_light.cycle_duration = duration

def set_tts(traffic_light: TrafficLight, tts:list[float]):
    traffic_light.time_to_switch = tts

    # def run(self):
    #     """Simulates the traffic light running through its states."""
    #     while True:
    #         time.sleep(self.state.value)
    #         self.next_state()

