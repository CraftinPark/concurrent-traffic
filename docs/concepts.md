### World Position vs Screen Position
world position is our own coordinate system. (0,0) represents the middle of the intersection. depending on the constants `WORLD_WIDTH` and `WORLD_HEIGHT` the bounds will change.\
screen position is the describing pixels. (0,0) represents the top left of the window, and depending on `SCREEN_WIDTH` and `SCREEN_HEIGHT` the size of the window will change.

### Route Position
vehicles do not have an cartesian x,y position. Instead they have a route position. Route position is a value in meters from 0 - t, where t is the total length of a route.

benefits:
- single parameter of displacement (arclength)
- manager will be working with routes rather than predicting vehicle pos/vel/direction

Routes have multiple segments of edges. For example it can be composed of a straight edge, a curved edge, and a straight edge. The route class has a function called `route_position_to_world_position` that is responsible for determining the x,y position.

### Command
A command is instructions that the Manager will send to a vehicle to make adjustments to its speed. The Manager only has control over the acceleration (gas pedal) and decceleration (brake pedal) and in theory the wheel of the vehicle. A command will be a piecewise function of time and acceleration. For example, the command can say:\
from 0-10 seconds, apply X acceleration.\
from 10-15 seconds, apply Y acceleration.\
The vehicle will keep this command and step through in it's time, and apply the acceleration.