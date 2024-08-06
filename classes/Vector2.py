from constants.initialisation import FPS
from typing import Tuple


class Vector2:
    x: float
    y: float

    # vectors change every second
    velocity: Tuple[float, float]

    def __init__(self, x: float, y: float, velocity: Tuple[float, float]):
        self.x = x
        self.y = y
        self.velocity = velocity

    def act(self, commands: list = None):
        """
        Funny idea of making a commands list
        Method will complete all the commands
        :param commands: if None, method will complete existing
        :return:
        """
        pass

    def move(self) -> None:
        """
        The method changes the coords of the vector in accordance with its velocity
        The method is assumed to be executed every frame
        """
        change = [self.velocity[0]/FPS, self.velocity[1]/FPS]
        self.x += change[0]
        self.y += change[1]

    def set_velocity(self, new_velocity: Tuple[float, float] = (0., 0.)):
        self.velocity = new_velocity

    def coordinates(self) -> tuple:
        return self.x, self.y

    def coordinates_list(self) -> list:
        return [self.x, self.y]

    def coordinates_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    def len(self) -> float:
        return (self.x**2+self.y**2)**0.5

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y,(0., 0.))

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y,(0., 0.))

    def __mul__(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return f"{self.coordinates()}"
