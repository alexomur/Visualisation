def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Dimension:
    value_SI: float
    value: str

    dim_name: str  # "s" for seconds or "m" for meters for example

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

    def toSI(self, arg: str | float = None) -> float:
        if arg is None:
            return self.value_SI

        arg = str(arg)
        s = arg.split(" ")
        x: float = float(s[0])
        if is_number(arg):
            return x
        dim: str = s[1].split(self.dim_name)[0]
        return x*self.prefixes[dim]

    def setValue(self, value: str):
        value_SI = self.toSI(value)
        self.value_SI = value_SI
        self.value = f"{value_SI} {self.dim_name}"

    def __float__(self):
        return self.value_SI

    def __int__(self):
        return int(self.value_SI)

    def __str__(self):
        return self.value

    def __bool__(self):
        return bool(self.value_SI)

    """
    It meant to create __add__, __sub__ and other methods 
    for every class
    """
