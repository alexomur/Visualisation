class Vector2:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coordinates(self) -> tuple:
        return self.x, self.y

    def coordinates_list(self) -> list:
        return [self.x, self.y]

    def coordinates_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    def len(self) -> float:
        return (self.x**2+self.y**2)**0.5

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)

    def __mul__(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return f"{self.coordinates()}"
