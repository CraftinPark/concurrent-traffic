# concurrent-traffic
concurrent-traffic is a project to create an algorithm that removes traffic lights given that all vehicles have self-driving technology. In practice, vehicles from all four directions can be moving at the same time, avoidings each other with a safe distance. The algorithm is run by a manager that communicates with cars approaching an intersection.

As part of this project is a traffic simulator made with pygame that gives us a means to provide input to the algorithm and a way to perceive the algorithm.

Priorities of the algorithm:
- Safety (avoids 100% collisions)
- Comfort (no rapid accelerations/sharp turns)
- Speed (faster and more efficient than a standard traffic light)