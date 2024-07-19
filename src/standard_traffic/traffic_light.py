from enum import Enum
import time

class TrafficState(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

    def next(self):
        if self == TrafficState.RED:
            return TrafficState.GREEN
        elif self == TrafficState.GREEN:
            return TrafficState.YELLOW
        elif self == TrafficState.YELLOW:
            return TrafficState.RED

class TrafficLight:
    state: TrafficState

    def __init__(self, red_duration=45, yellow_duration=5, green_duration=45, initial_state=TrafficState.RED) -> None:
        if not isinstance(initial_state, TrafficState):
            raise ValueError("initial_state must be an instance of TrafficState")
        self.state = initial_state
        self.durations = {
            TrafficState.RED: red_duration,
            TrafficState.YELLOW: yellow_duration,
            TrafficState.GREEN: green_duration,
        }

    def next_state(self):
        self.state = self.state.next()

    def get_state(self):
        return self.state
    
    def set_state(self, state: TrafficState):
        self.state = state
    
    def set_duration(self, state: TrafficState, duration):
        """To use: config.set_duration(TrafficLight.RED, 40)"""
        if state in self.durations:
            self.durations[state] = duration
        else:
            raise ValueError(f"{state} is not a valid traffic light state.")
        
    def get_duration(self, state):
        if not isinstance(state, TrafficState):
            raise ValueError("state must be an instance of TrafficState")
        return self.durations[state]

    def run(self):
        """Simulates the traffic light running through its states."""
        while True:
            time.sleep(self.state.value)
            self.next_state()

    def run(self, cycles: int = 3):
        for _ in range(cycles):
            current_state = self.get_state()
            duration = self.get_duration(current_state)
            time.sleep(duration)
            self.next_state()