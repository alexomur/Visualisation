def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Dimension:
    value_SI: float
    value: str
    power: int

    # "s" for seconds or "m" for meters for example
    # "s^2" for power of 2
    dim_name: str

    prefixes: dict[str, float] = {
        "T": 1e12,
        "G": 1e9,
        "M": 1e6,
        "k": 1e3,
        "h": 1e2,
        "da": 1e1,
        "": 1,
        "d": 1e-1,
        "c": 1e-2,
        "m": 1e-3,
        "mk": 1e-6,
        "n": 1e-10,
        "p": 1e-12
    }

    def __init__(self, x: str | float, power: int = 1):
        self.setValue(x, power)

    def toSI(self, arg: str | float = None) -> float:
        if arg is None:
            return self.value_SI
        if is_number(arg):
            return float(arg)

        arg = str(arg)
        s = arg.split(" ")
        x: float = float(s[0])
        power: int = int(s[1].split("^")[1])
        dim: str = s[1].split(self.dim_name)[0]
        return x * (self.prefixes[dim]**power)

    def setValue(self, value: str | float, power: int = 1) -> None:
        value_SI = self.toSI(value)
        self.value_SI = value_SI
        self.value = f"{value_SI} {self.dim_name}"

        if power != 1:
            value += f"^{power}"
        self.power = power

    def __float__(self):
        return self.value_SI

    def __int__(self):
        return int(self.value_SI)

    def __str__(self):
        return self.value

    def __bool__(self):
        return bool(self.value_SI)

    def __add__(self, other):
        if isinstance(other, Dimension):
            if type(self) == type(other) and self.dim_name == other.dim_name:
                return type(self)(self.value_SI + other.value_SI, self.power)
            else:
                raise TypeError(f"Unsupported operand type(s) for +: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")
        else:
            raise TypeError(f"Unsupported operand type(s) for +: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")

    def __sub__(self, other):
        if isinstance(other, Dimension):
            if type(self) == type(other):
                return type(self)(self.value_SI - other.value_SI)
            else:
                raise TypeError(f"Unsupported operand type(s) for -: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")
        else:
            raise TypeError(f"Unsupported operand type(s) for -: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")

    # TODO: Add the ability to change the power of a number using multiplication and division
    # TODO: Add the ability to multiply and divide different dimensions (and change dim_name)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_obj = type(self)(self.value_SI * other)
            return new_obj
        else:
            raise TypeError(f"Unsupported operand type(s) for *: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return type(self)(self.value_SI / other)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: {self.dim_name} ('{type(self)}') and {other.dim_name} ('{type(other)}')")
