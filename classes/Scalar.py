def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def split_once(expr: str) -> list:
    """
    Splits the expression at the first outermost '/' found.

    :param expr: The expression to split.
    :return: A list containing two parts of the expression split at the first outermost '/'.
    """
    depth = 0
    for i, char in enumerate(expr):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == '/' and depth == 0:
            return [expr[:i], expr[i + 1:]]

    if expr[0] == '(' and expr[-1] == ')' and expr.count('(') == expr.count(')') == 1:
        return split_once(expr[1:-1])

    return [expr, '']


def split_division(div: str, reverse_divider: bool = True) -> list:
    """
    Recursively splits the division expression into nested lists.

    :param div: The division expression to split.
    :param reverse_divider: If True, reverse the order of division for inner parts.
    :return: A nested list representing the split expression.
    """
    if not ('/' in div):
        return [div]
    sp = split_once(div)
    sp[0] = split_division(sp[0])
    sp[1] = split_division(sp[1])
    if reverse_divider:
        sp[1] = list(reversed(sp[1]))
    return sp


def join_expression(nested_list) -> str:
    """
    Joins a nested list into a string with multiplication for inner elements.

    :param nested_list: The nested list to join.
    :return: A string representing the joined expression.
    """
    if isinstance(nested_list, str):
        return nested_list
    elif isinstance(nested_list, list):
        if len(nested_list) == 1:
            return join_expression(nested_list[0])
        else:
            return '(' + '*'.join(join_expression(item) for item in nested_list) + ')'

class Dimension:
    dim_full: str
    numerator: str
    divider: str

    def __init__(self, dim_full: str):
        dim_full = self.normalize(dim_full)
        self.dim_full = dim_full
        if not ('/' in dim_full):
            self.numerator = dim_full
            self.divider = ""
            return
        if dim_full.count('/') == 1:
            self.numerator = ''.join(dim_full.split('/')[0])
            self.divider = ''.join(dim_full.split('/')[1])
            return
        pass


    @staticmethod
    def normalize(div: str) -> str:
        """
        Will convert the string of the form (a/b)/(c/d) to the form (a*d)/(b*c)
        :param div: The expression to normalize
        :return: Normalized expression
        """
        div_list = split_division(div)
        return '/'.join(join_expression(item) for item in div_list)


class Scalar:
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

    def __init__(self, x: str | float, dim_name: str, power: int = 1):
        self.dim_name = dim_name
        self.setValue(x, power)

    def toSI(self, arg: str | float = None) -> float:
        if arg is None:
            return self.value_SI
        if is_number(arg):
            return float(arg)

        arg = str(arg)
        s = arg.split(" ")
        x: float = float(s[0])
        power: int = int(s[1].split("^")[1]) if "^" in s[1] else 1
        dim: str = s[1].split(self.dim_name)[0]
        return x * (self.prefixes[dim]**power)

    def setValue(self, value: str | float, power: int = 1) -> None:
        self.value_SI = self.toSI(value)
        self.value = f"{value} {self.dim_name}"
        if power != 1:
            self.value += f"^{power}"
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
        if isinstance(other, Scalar):
            if self.dim_name == other.dim_name:
                return Scalar(self.value_SI + other.value_SI, self.dim_name, self.power)
            else:
                raise TypeError(f"Unsupported operand type(s) for +: '{self.dim_name}' and '{other.dim_name}'")
        else:
            raise TypeError(f"Unsupported operand type(s) for +: '{self.dim_name}' and '{type(other)}'")

    def __sub__(self, other):
        if isinstance(other, Scalar):
            if self.dim_name == other.dim_name:
                return Scalar(self.value_SI - other.value_SI, self.dim_name, self.power)
            else:
                raise TypeError(f"Unsupported operand type(s) for -: '{self.dim_name}' and '{other.dim_name}'")
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{self.dim_name}' и '{type(other)}'")

    @staticmethod
    def simplify_dim(dim: str) -> str:
        if "/" in dim:
            pass



    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Scalar(self.value_SI * other, self.dim_name, self.power)
        elif isinstance(other, Scalar):
            new_dim_name = f"{self.dim_name}*{other.dim_name}"
            new_dim_name = self.simplify_dim(new_dim_name)
            new_value_SI = self.value_SI * other.value_SI
            return Scalar(new_value_SI, new_dim_name)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: '{self.dim_name}' and '{type(other)}'")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Scalar(self.value_SI / other, self.dim_name, self.power)
        elif isinstance(other, Scalar):
            new_dim_name = f"{self.dim_name}/({other.dim_name})"
            new_dim_name = self.simplify_dim(new_dim_name)
            new_value_SI = self.value_SI / other.value_SI
            return Scalar(new_value_SI, new_dim_name)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: '{self.dim_name}' and '{type(other)}'")

# Примеры использования
s1 = Scalar(3, 'm')
s2 = Scalar(4, 's')
s3 = s1 * s2  # Должно создать новый Scalar с размерностью 'm*s'
s4 = s1 / s2  # Должно создать новый Scalar с размерностью 'm/s'

print(s3)  # Output: 12.0 m*s
print(s4)  # Output: 0.75 m/s

print(s3 / s4)  # Output: 16.0 s^2
