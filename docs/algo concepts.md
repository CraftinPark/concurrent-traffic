Scratch notes from past:

### Collisions array. Tree problem

the root of the tree is the current trajectories. The number of collisions represents the number of the node.
Each leaf of the tree is an adjustment that reduces the number of collisions.

notes:
The idea has flaws, for example, it will miss the optimal solution where carA slows down a little and carB speeds up a little. When adjusting carA's speed, it will move it to totally avoid carB.

can this be turned into a bipartite graph? where one side is cars on the X line and other side is cars on the Y line?

will have to try this approach to see it's effectiveness.

### Priority to closest to intersection

To simplify the problem and as a proof of concept, we will start by a simple approach, where the priority goes to the car that is closest to the intersection.
If car1 is closer to the intersection than car2, and car1 and car2 are in a collision course, then car2 must yield and slow down it's speed.
If the resulting speed change of car2 results in a new collision course with car3, and car2 is closer to the intersection, then car3 will have to slow down.
if in the collision course between car2 and car3, car3 was closer to the intersection, then car2 will have to yield yet again and slow down it's speed.

cautionary notes:
if car1 is closer to the intersection than car2, but car2 had a faster velocity, it may be the case that after the calculation, car2 is closer to the intersection. Perhaps the distance to the intersection should be based on the future? metric of: "who will get to the intersection first?"