from . import Dimension
class Meters(Dimension):
    dim_name = "m"

    def __init__(self, x: str | float):
        self.setValue(x)

    def __add__(self, other):
        return Meters(self.value_SI + other.value_SI)

    def __sub__(self, other):
        return Meters(self.value_SI - other.value_SI)

    def __mul__(self, other):
        return Meters(self.value_SI * other.value_SI)

    def __truediv__(self, other):
        return Meters(self.value_SI / other.value_SI)
