from traffic_light import TrafficLight, next_state, set_state, set_cycle_dur, set_tts, TrafficState
from math import floor
import itertools
from classes.edge import TrafficState

class TrafficMaster:
    traffic_lights: dict[str, list[TrafficLight]] = {}
    traffic_types: dict[str, dict[TrafficState, int]] = []

    def __init__(self, types: list[tuple], t_lights: list[TrafficLight]) -> None:
        """Initialize all the differnet traffic lights in each list
        Have a central time, then send requests for each traffic light to switch light"""
        for t_type in types:
            self.traffic_types[t_type[0]] = {TrafficState.RED : t_type[1], TrafficState.YELLOW : t_type[2], TrafficState.GREEN: t_type[3], "initial_state": t_type[4]}
            self.traffic_lights[t_type[0]] = []
        for key in self.traffic_lights.keys():
            for light in t_lights:
                if light.identifier == key:
                    self.traffic_lights[key].append(light)
                    set_state(light, t_type[4])
                    set_cycle_dur(light, sum(t_type[1:-1]))
                    set_tts(light, list(itertools.accumulate(t_type[1:-1])))

def t_master_event_loop(traffic_master: TrafficMaster, delta_time: int) -> None:
    for l_type, light_list in traffic_master.traffic_lights.items():
        for light in light_list:
            light.time_in_state += delta_time
            # delta_time - floor(delta_time/light.cycle_duration) * light.cycle_duration
            if any(light.time_in_state > c and abs(light.time_in_state - c) < 0.001 for c in light.time_to_switch):
                next_state(light)
