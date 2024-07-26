from .traffic_light import TrafficLight, next_state, set_state, set_cycle_dur, set_tts, reset_time_in_state, get_state, TrafficState
from math import floor
import itertools

class TrafficMaster:
    traffic_lights: dict[str, list[TrafficLight]] = {}
    traffic_types: dict[str, dict] = []
                        

    def __init__(self, types: list[tuple], t_lights: list[TrafficLight]) -> None:
        """Initialize all the differnet traffic lights in each list
        Have a central time, then send requests for each traffic light to switch light"""
        self.traffic_types, self.traffic_lights = {}, {}
        for t_type in types:
            self.traffic_types[t_type[0]] = {TrafficState.RED : t_type[1], TrafficState.YELLOW : t_type[2], TrafficState.GREEN: t_type[3], "initial_state": t_type[4], "duration_list" : [t_type[1], t_type[2], t_type[3]]}
            self.traffic_lights[t_type[0]] = []
        for key in self.traffic_lights.keys():
            for light in t_lights:
                if light.identifier == key:
                    self.traffic_lights[key].append(light)
                    reset_time_in_state(light)
                    set_state(light, t_type[4])
                    set_cycle_dur(light, sum(self.traffic_types[key]["duration_list"]))
                    # set_tts(light, list(itertools.accumulate(self.traffic_types[key]["duration_list"])))
                    set_tts(light, {k: v for k, v in self.traffic_types[key].items() if k != 'initial_state' and k != 'duration_list'})

def t_master_event_loop(traffic_master: TrafficMaster, delta_time: int) -> None:
    for l_type, light_list in traffic_master.traffic_lights.items():
        for light in light_list:
            light.time_in_state += (delta_time- light.prev_dt)
            light.prev_dt = delta_time
            # delta_time - floor(delta_time/light.cycle_duration) * light.cycle_duration

            # next_index = (light.state.value + 1) % TrafficState.get_num_states() # 2 -> 3 , 3-> 0
            # next_tts = light.time_to_switch[next_index - 1]  # doesn't work unless self.time_to_switch is a dictionary
            # # TrafficState.RED.value returns 1

            next_t_state = light.state.get_next_state(light.state.value)
            if light.time_in_state > light.time_to_switch[next_t_state]:
            # if any(light.time_in_state > c and abs(light.time_in_state - c) < 0.1 for c in light.time_to_switch):
                print(l_type, "delta_time", delta_time, "time in loop", light.time_in_state, "time_to_switch", light.time_to_switch)
                # if 0 < light.time_in_state - light.cycle_duration < 0.1:
                # print("changing to the next loop. cycle_duration is ", light.cycle_duration)
                # print(l_type, "next state:", get_state(light))
                next_state(light)
