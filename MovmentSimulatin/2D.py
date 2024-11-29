import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

# Vector class for vector operations
class Vector:
    def __init__(self, components: List[float]) -> None:
        self.vec = components

    def __add__(self, other: "Vector") -> "Vector":
        if len(self.vec) != len(other.vec):
            raise ValueError("Vectors must be of the same dimension")
        return Vector([a + b for a, b in zip(self.vec, other.vec)])

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self.vec) != len(other.vec):
            raise ValueError("Vectors must be of the same dimension")
        return Vector([a - b for a, b in zip(self.vec, other.vec)])

    def magnitude(self) -> float:
        return sum(a**2 for a in self.vec) ** 0.5

    def normalize(self) -> "Vector":
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector([a / mag for a in self.vec])

    def __mul__(self, scalar: float) -> "Vector":
        return Vector([a * scalar for a in self.vec])

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __getitem__(self, index: int) -> float:
        return self.vec[index]

    def __setitem__(self, index: int, value: float) -> None:
        self.vec[index] = value

    def __str__(self) -> str:
        return f"Vector({self.vec})"


class Obj:
    def __init__(self, 
                 mass: float, 
                 vel: Vector, 
                 force: Vector, 
                 ident: str, 
                 env: "Environment") -> None:
        """
        Represents a physical object in the environment.
        
        Parameters:
        - mass: Mass of the object (kg)
        - vel: Initial velocity vector (m/s)
        - force: Constant force applied to the object (N)
        - ident: Unique identifier for the object
        - env: Environment the object belongs to
        """
        self.mass = mass
        self.vel = vel
        self.force = force
        self.ident = ident
        self.place = Vector([0.0, 0.0])  # Initial position
        self.env = env
        self.env.add_obj(self)
        self.acc = self.calculate_acceleration()
        self.path = []  # Record of the object's position over time

    def calculate_acceleration(self) -> Vector:
        gravity_effect = Vector([0.0, -self.env.gravity * self.mass])
        net_force = self.force + gravity_effect + self.env.wind
        return Vector([net_force[i] / self.mass for i in range(len(net_force.vec))])

    def update_place(self, time_step: float = 0.1) -> None:
        """
        Updates the position and velocity of the object based on the current acceleration.
        """
        self.place = self.place + self.vel * time_step + self.acc * (0.5 * time_step**2)
        self.vel = self.vel + self.acc * time_step
        self.acc = self.calculate_acceleration()
        self.path.append((self.place[0], self.place[1]))

    def __str__(self) -> str:
        return (f"Obj(id={self.ident}, place={self.place}, "
                f"vel={self.vel}, acc={self.acc})")


class Obstacle:
    def __init__(self, position: Vector, radius: float) -> None:
        """
        Represents a circular obstacle in the environment.
        
        Parameters:
        - position: Center position of the obstacle (Vector)
        - radius: Radius of the obstacle
        """
        self.position = position
        self.radius = radius

    def check_collision(self, obj: Obj) -> bool:
        """
        Checks if an object is colliding with the obstacle.
        """
        distance = ((obj.place[0] - self.position[0])**2 + (obj.place[1] - self.position[1])**2) ** 0.5
        return distance <= self.radius


class Environment:
    def __init__(self, gravity: float = 9.81, wind: Vector = Vector([0.0, 0.0])) -> None:
        """
        Environment containing objects, obstacles, and simulation parameters.
        
        Parameters:
        - gravity: Gravitational constant (m/s^2)
        - wind: Wind force applied globally to all objects (Vector)
        """
        self.gravity = gravity
        self.wind = wind
        self.objects = []
        self.obstacles = []

    def add_obj(self, obj: Obj) -> None:
        self.objects.append(obj)

    def add_obstacle(self, position: Vector, radius: float) -> None:
        self.obstacles.append(Obstacle(position, radius))

    def simulate_movement(self, time_step: float = 0.1, steps: int = 100, ident: Optional[str] = None) -> None:
        """
        Simulates the movement of all or specific objects over a given number of steps.
        
        Parameters:
        - time_step: Duration of each simulation step (s)
        - steps: Number of simulation steps
        - ident: Identifier of a specific object to simulate (default: None for all objects)
        """
        objects_to_simulate = [self.get_obj(ident)] if ident else self.objects

        for step in range(steps):
            print(f"Step {step + 1}:")
            for obj in objects_to_simulate:
                obj.update_place(time_step)
                for obstacle in self.obstacles:
                    if obstacle.check_collision(obj):
                        print(f"Collision detected for {obj.ident} with obstacle at {obstacle.position}")
                        obj.vel = obj.vel * -0.5  # Simple collision response
                print(obj)
            print("\n")

    def get_obj(self, ident: str) -> Obj:
        for obj in self.objects:
            if obj.ident == ident:
                return obj
        raise ValueError(f"Object with id {ident} not found")

    def plot_paths(self) -> None:
        """
        Plots the paths of all objects in the environment.
        """
        for obj in self.objects:
            path = list(zip(*obj.path))
            plt.plot(path[0], path[1], label=obj.ident)
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.title("Object Paths")
        plt.legend()
        plt.grid()
        plt.show()


# Example Usage
if __name__ == "__main__":
    env = Environment(wind=Vector([0.56, 0.0]))

    # Create objects
    ball = Obj(
        mass=10.0,
        vel=Vector([5.0, 15.0]),
        force=Vector([0.0, -5.0]),
        ident="Ball1",
        env=env,
    )

    # Add obstacle
    env.add_obstacle(Vector([20.0, 0.0]), radius=2.0)

    # Simulate movement
    env.simulate_movement(time_step=0.1, steps=300)
    env.plot_paths()
