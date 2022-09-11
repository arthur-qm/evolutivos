# Initial goal
Making 'predators' evolve along with 'preys'
## What will the environment be like?
There will be a few predators and a few preys on the screen and each
iteration will have a time limit
### Scorings

The predator gets score by getting close to preys
The predator gets a lot of score from eating preys

The prey gets its score by its mean distance from the closest predator for each time tick

### Movement
At each tick, the neural network will output a "decision" of 2 elementos. For the first element,
If the decision is less than 0.25, it will activate "turn left"
Else if it is less than 0.75, it will do nothing
Else it will activate "turn right"
For the second element, the same thing will happen, but instead of 0.25 and 0.75 we'll have 0.3 and 0.7 and instead of turning we'll have "accelerate" and "decelerate" a

To understand what these do, we'll analyse the move function first
It keeps the magnetude of the acceleration and velocity under control and adds the acceleration vector to the velocity vector (the same thing with position and velocity).

Accelerate increases the magneture of the acceleration vector by "accelerationIncrease" and so does decelerate

Turn left and turn right abruptly modify the acceleration direction
by "turning angle"



### NNs
Use of the neat model
Predators will have a lot of sensors in the direction they face
Preys will have spaced sensors in all directions

### How will individuals and generations work?
For each generation, there will be X different simulations
Each of them has 1 predator and Y preys (Y=5). 

## Current rendering
For now, display an arbitrary simulation of the current generation