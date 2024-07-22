from enum import Enum, auto
from classes.edge import Edge
from classes.node import Node

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

    def next_state(self):
        self.state = self.state.next()
        new_state = self.get_state
        self.edge.change_state(new_state)
        self.reset_time_in_state()
    
    def reset_time_in_state(self):
        self.time_in_state = 0

    def get_state(self) -> TrafficState:
        return self.state
    
    def set_state(self, state: TrafficState):
        self.state = state
        self.edge.change_state(state)

    def set_cycle_dur(self, duration: int):
        if duration < 1:
            raise ValueError(f"Cycle duration cannot be less than 1.")
        self.cycle_duration = duration
    
    def set_tts(self, tts:list[float]):
        self.time_to_switch = tts

    # def run(self):
    #     """Simulates the traffic light running through its states."""
    #     while True:
    #         time.sleep(self.state.value)
    #         self.next_state()

