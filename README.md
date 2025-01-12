# *Physics Simulation in Python* #
This project is a Python-based simulation framework for modeling physical objects, their interactions, and their environment. It includes features for simulating movement under forces, handling collisions with obstacles, and visualizing the trajectories of objects.

## Features
* Vector Class: A utility for vector operations like addition, subtraction, normalization, and scalar multiplication.
* Physical Objects (Obj):
    Simulates objects with mass, velocity, and applied forces.
    Calculates acceleration based on net forces, including gravity and wind.
    Tracks object trajectories over time.

* Environment:
Contains objects, obstacles, and global forces like gravity and wind.
Manages the simulation of movement and interactions.

* Obstacles:
Circular obstacles that detect collisions with objects.
Simple collision response for interactions.

* Visualization:
Plots the paths of objects during simulation using matplotlib.


## Installation

Clone the repository
```bash
git clone https://github.com/your-username/physics-simulation.git
cd physics-simulation
```

Install required dependencies
```bash
pip install matplotlib
```


## usage

Initialize the environment:
```python
from simulation import Environment, Obj, Vector
env = Environment(wind=Vector([0.56, 0.0]))
```

Add objects:

```python
ball = Obj(
    mass=10.0,
    vel=Vector([5.0, 15.0]),
    force=Vector([0.0, -5.0]),
    ident="Ball1",
    env=env,
)
```

Add obstacles:
```python
env.add_obstacle(Vector([20.0, 0.0]), radius=2.0)
```

Simulate and visualize:
```python
env.simulate_movement(time_step=0.1, steps=300)
env.plot_paths()
```


## Classes Overview
`Vector`
A utility class for handling vector operations.

`Obj`
Represents a physical object with properties such as mass, velocity, and forces acting upon it.

`Environment`
Defines the simulation space, including gravity, wind, objects, and obstacles.

`Obstacle`
Models circular obstacles with collision detection.


## Requirements
Python 3.7+
matplotlib

# Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.
  
