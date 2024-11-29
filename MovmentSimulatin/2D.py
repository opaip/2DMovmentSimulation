from typing import List

# Vector class to handle vector operations
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

    def dot(self, other: "Vector") -> float:
        if len(self.vec) != len(other.vec):
            raise ValueError("Vectors must be of the same dimension")
        return sum(a * b for a, b in zip(self.vec, other.vec))

    def magnitude(self) -> float:
        return sum(a**2 for a in self.vec) ** 0.5

    def __getitem__(self, index: int) -> float:
        return self.vec[index]

    def __setitem__(self, index: int, value: float) -> None:
        self.vec[index] = value

    def __mul__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply a Vector by a scalar (int or float)")
        return Vector([a * scalar for a in self.vec])

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __str__(self) -> str:
        return f"Vector({self.vec})"

# Object class for physical simulation
class Obj:
    def __init__(self, 
                 mass: float, 
                 vel: Vector, 
                 force: Vector, 
                 ident: str, 
                 env: "Environment") -> None:
        self.mass = mass
        self.vel = vel
        self.force = force
        self.ident = ident
        self.place = Vector([0.0, 0.0])  # Initial position (x, y)
        self.env = env
        self.env.add_obj(self)
        self.acc = self.calculate_acceleration()

    def calculate_acceleration(self) -> Vector:
        gravity_effect = Vector([0.0, -self.env.gravity * self.mass])
        net_force = self.force + gravity_effect
        return Vector([net_force[i] / self.mass for i in range(len(net_force.vec))])

    def update_place(self, time_step: float = 0.1) -> None:
        self.place = self.place + self.vel * time_step + self.acc * (0.5 * time_step**2)
        self.vel = self.vel + self.acc * time_step
        self.acc = self.calculate_acceleration()

    def __str__(self) -> str:
        return (f"Obj(id={self.ident}, place={self.place}, "
                f"vel={self.vel}, acc={self.acc})")

# Environment class to manage objects and simulate movement
class Environment:
    def __init__(self, gravity: float = 9.81) -> None:
        self.gravity = gravity
        self.objects = []

    def add_obj(self, obj: Obj) -> None:
        self.objects.append(obj)

    def get_obj(self, ident: str) -> Obj:
        for obj in self.objects:
            if obj.ident == ident:
                return obj
        raise ValueError(f"Object with id {ident} not found")

    def simulate_movement(self, time_step: float = 0.1, steps: int = 100, ident: str = None) -> None:
        if ident:
            objects_to_simulate = [self.get_obj(ident)]
        else:
            objects_to_simulate = self.objects

        for step in range(steps):
            print(f"Step {step + 1}:")
            for obj in objects_to_simulate:
                obj.update_place(time_step)
                print(obj)
            print("\n")

# Example Usage
if __name__ == "__main__":
    env = Environment()

    # Create objects
    obj1 = Obj(
        mass=10.0,
        vel=Vector([5.0, 10.0]),
        force=Vector([0.0, -20.0]),
        ident="Ball1",
        env=env,
    )

    # Simulate movement
    env.simulate_movement(time_step=0.1, steps=1000, ident="Ball1")
