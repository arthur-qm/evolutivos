# Evolution of preys and predators

This project intends to mimic the basics of the ecological relationship between preys
and predators in a broad sense. 

# First steps

In a first glance, the problem seems too hard, even if we only consider the most basic elements of
the natural dynamic between a prey and its predator. Because of this, I am currently working at a smaller 
problem first, after which I will be able to develop whatever I want more easily.  

# 1) Predator evolution

The problem I am currently trying to solve can be stated as follows.

## 1.1) Ambience

We have a 800x800 screen, in which there are individuals, which are either preys or predators.
Preys are represented by a small green circle, and predators by a red, bigger one. We say the simulations has "ticks". This means
the number of iterations it has - in case the simulation is being shown in a screen, this is coincides with the total number of
frames throughout all the course of a simulation.

[*image*]

### 1.1.1) Movement

All of the individuals have the following key properties (although for the problem I'm currently solving, most of these only make
sense for the predator, but that will be explained later)
- Position (obviously)
- Speed vector
- Acceleration vector
- A director vector, which, at all instants of time, is parallel to the acceleration vector (this means that it can have the same direction or the 
opposite one) and represents the direction the individual is facing. 
- A scalar floating point variable "acc", whose function, along with the director vector, is to construct the acceleration vector. Namely,
at all instants of time, we have the value of "acc" and the director vector and with them we calculate the acceleration vector
by multiplying the scalar "acc" by the director vector. The benefit of doing things this way is that the individual behaves in a smoother way.
In fact, if the acceleration mechanic was not done this way, then the direction the individual is facing could abruptly change. The code which
decides acc value's for each instant of time (more into that later) is such that its absolute value never exceeds a given limit which is defined
in the config.py value. 

Therefore, as it can be seen on the function move() of the Individual class of the individual.py file, at each tick of the game, all individuals
move like this (right after their new acc value and director vector are decided for that tick. But we'll get into this in a minute):
- Firstly, the acceleration vector is calculated by multiplying the current director vector of the individual (which, by the way, is unitary at all instants
of time) by the acc variable (which, as explained, can be any real number inside a limited range).
- Then, we add the acceleration vector to the speed vector. And if after this sum the magnetude of the speed vector is above a certain limit given
on the config.py file, it is then reduced back to the limit.
- After this, the position is updated by the speed vector.

With all that said, the movement mechanic works as follows:

A) When controlled manually with the keyboard

At each time tick, pygame listens for keys. If a right key is pressed, at that tick the function turn_right() (a more adequate name would be turn
clockwise). Analogously, if a left key is pressed, turn_left() is called. If the up key is pressed, accelerate() is called. And the same happens with
the down key and decelerate(). More into these functions after this topic.

B) When controlled by a random decider

At each time tick, two random values between 0 and 1 are decided. If the first one is lower than 0.3, it turns left. If its higher than 0.7, it turns right.
(this leaves a margin for doing nothing). Similarly for the acceleration, it calls decelerate() if the second random variable is lower than 0.3 and accelerate() if its higher than 0.7

C) When controlled by a neural network

Based on the enviromental inputs (which will be discussed later), it returns two values between 0 and 1. And just like on (B), at each
tick it decides which functions to call based on these two values.


Lastly, the accelerate, decelerate, turn_left and turn_right functions are defined like this:
accelerate and decelerate increase or decrease the value of the scalar acc by a constant. We also make sure acc's absolute value never exceeds a limit, as
said previously.
turn_right and turn_left make the director vector of the individual get abruptly rotated by a constant angle clockwise or anti-clockwise respectively.

Hence, depending on the mechanic we're taking into account (A, B or C), at each tick we call these four functions in a certain way, which changes the director
vector and the acc value. After that we call the "move()" method, which firstly calculates the acceleration vector by taking into account 
the current acc and director vector and then works as aforementioned.

### 1.1.2) Limitations

By a certain offset from the border of the pygame window, there are four walls which inhibt individuals from moving outside the screen.
This means that at all times, they're stuck there. The wall is implemented by checking if the position (right after updating it) has x or y
components that exceed the barrier. If they do, the coordinates are forced to be equal to the limiting barriers' ones.

### 1.1.3) The eye of the predator

Around the director vector, there are twenty rays (line segments), divided into two groups of 10 (one associated with the preys and the other
associated with the walls). Each ray represents part of the vision of the predator. Also, the length of the 20 segments is the same and each
group of 10 is evenly spaced (considering their angular separations), as seen on the image:

[Image]

Based on the intersection of these rays and the circles which represent the preys / the walls, a "distance" value is computed. Here's how this
"distance" is calculated for each of the 20 rays:

The first group of 10 deals with seeing the preys. If the line segment does not intersect any prey green circles, the value zero is associated
with it. If it intersects, then the euclidean distance between the center of the predator and the center of the prey is considered. We then
subtract this distance by the sum of the radiuses of the prey and
predator and divide this result by sqrt(range^2+rprey^2) where range is the length of the line segment and rprey is the radius of the prey circle.
So from this we get a value x from 0 to 1. Now, consider z=1-x. I did this so that if the prey is at the highest distance possible but still
within the vision range, then x=1 and z=0. Also, if it is touching the predator, then x is close to 0 and z is close to one. We could stop 
here and say that, for the case in which the ray touches a prey, the value associated with the ray is this z. However, if we did that, then 
the two following situations would give us similar values
- The ray sees no prey. So its value is zero.
- The prey is at the extremity of the ray. So its value is close to zero.
So these situations would be treated in similar ways by a mathematical model. To prevent this, we say that, instead of z, we'll work with 3z+1
This means that the value associated with the ray abruptly jumps from 0 to 1 when the prey starts to touch it. Moreover, the coefficient 3 makes t
he distance along the ray more evident to the mathematical model.

The second group of 10 rays deals with the distances to the walls. We consider the distance from the center of the predator's circle to the
point of the intersection between the ray segment and the wall segment subtracted by the predator's radius. 
From here, we define x and z in a similar way as the previous paragraph
and also associate the value 3z+1 with the ray.

Here are two images to make this reasoning more clear:

[Image prey] [Image wall] 

Notice that the rays overlap each other. Its as if the predator had ten eyes, and for each of them, two variables would be its vision input: the 
distance function for the prey and for the wall

At each tick, these 20 values (along with other information) are used as input to the neural network of the predator, whose main function is to do as 
described in (B) of section 1.1.1 and decide which of the 4 movement functions described in the end of section 1.1.1 to call.

### 1.1.4) Energy and digestion of the predator

The predator has a digestion variable, which is zero initially.
The predator eats a prey when their circles collide. When this happens, the prey dissapears. Also, the digestion variable increases by a constant C1.
For each tick, the digestion decreases by a constant C2. If the variable digestion is positive, but lower than a constant C3, a variable called energy increases
by C2. If at a tick, the variable digestion is higher than C3 (e.g. when it eats too much preys at a short amount of time), it "vomits" the excedent and the
digestion variable is set back to C3. When digestion gets lower than 0, it
immeadetely gets set back to 0.

The predator has an energy variable, which is C4 initially. At each tick, the energy decreases by C5 + C6 * velocity
(C5 comes from the cost to mantain the body functions and C6 comes from the energy spent to move ). If a prey is being digested, then, as already said, energy
will increase by C2. Also, the energy cant exceed C7. Energy over C7 is "dissipated".

### 1.1.5) Initial and end conditions

The simulation starts with a single predator and 30 preys spawning at a random place of the screen. The predator starts with a random speed, direction and
acceleration. The preys have their speed and acceleration at zero at all instants, so their initial position is mantained throughout the whole simulation.
The simulation ends when one of these two happen:
- The predator's energy ends.
- There are no longer any preys left.

## 1.2) The fitness function

Given all of what we've said, what would be a nice function for measuring how well a predator went at a given simulation? 
Here, we'll try to maximize "the sum of all values of energy during all game ticks". This makes sense if you think of it
"living with the most possible comfort for the maximum amount of time".

## 1.3) The neural network

The neural network is fixed and composed of four layers. The input layer has 25 neurons. 20 of them are the values returned by the 20 vision rays.
Other one is the component of the speed parallel to the director vector. The twentieth second is the perpendicular component of the speed. The twientieth
third is the acc variable (these are converted to values from -1 to 1 considering the max speed and acceleration). The twientieth fourth is the hunger and the
last one is the energy (these two are converted to values from 0 to 1). The
first hidden layer contains 5 neurons and the second contains 3. Each of the input neurons is connected to each of the first hidden layer's
neurons. Each connection has a weight associated with it. Each neuron (starting from the hidden layer) has a bias. So for a given neuron at the next layer,
we consider the value of the sum of the weights of the edges incident to it multiplied by the respective neuron value. And to this we add a bias. Take this value, and
apply the sigmoid function at it, which converts it to a value in the interval (0, 1). This final value will then be relayed into the next layer by the same rule.
The fourth layer (output) has two neurons (two outputs from 0 to 1). For each of these, we consider what was said at 1.1.1B.

## 1.4) The genetic algorithm

We start with a certain amount of random neural networks (which are our individuals for the genetic algorithm), meaning random weights and biases. For each generation,
we run a simulation for each of the current individuals (neural networks) and rank all of them based on their fitnesses. We use deap for handling the GA and make crossovers
and mutations.
