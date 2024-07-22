from traffic_light import TrafficLight, TrafficState
from math import floor
import itertools

class TrafficMaster:
    traffic_lights: dict[str, list[TrafficLight]] = {}
    traffic_types: dict[str, dict[TrafficState, int]] = []

    def __init__(self, types: list[tuple], traffic_lights: list[TrafficLight]) -> None:
        """Initialize all the differnet traffic lights in each list
        Have a central time, then send requests for each traffic light to switch light"""
        for t_type in types:
            self.traffic_types[t_type[0]] = {TrafficState.RED : t_type[1], TrafficState.YELLOW : t_type[2], TrafficState.GREEN: t_type[3], "initial_state": t_type[4]}
            self.traffic_lights[t_type[0]] = []
        for key in t_type.keys():
            for light in traffic_lights:
                if light.identifier == key:
                    self.traffic_lights[key].append(light)
                    light.set_state(t_type[4])
                    light.set_cycle_dur(sum(t_type[1:-1]))
                    light.set_tts(list(itertools.accumulate(t_type[1:-1])))

    def sequence(self, delta_time: int) -> None:
        for l_type, light_list in self.traffic_lights.items():
            # same durations
            for light in light_list:
                light.time_in_state += delta_time
                # delta_time - floor(delta_time/light.cycle_duration) * light.cycle_duration
                if any(abs(light.time_in_state - c) < 0.001 for c in light.time_to_switch):
                    light.next_state()
