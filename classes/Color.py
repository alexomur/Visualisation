from typing import NoReturn


class Color:
    rgb: tuple[int, int, int] = None
    hex: str = None
    visible: bool = True

    def __init__(self, rgb: tuple[int, int, int] = None, hex: str = None, hex_value: str = None):
        if hex and hex_value and hex != hex_value:
            raise TypeError(f"hex '{hex}' and hex_value '{hex_value}' do not match")
        if not hex:
            hex = hex_value

        if rgb is None and hex is None:
            raise TypeError(f"__init__ expected at least 1 argument, got 0")
        elif rgb and hex:
            if hex != self.toHex(rgb):
                raise ValueError(f"rgb '{rgb}' and hex '{hex}' do not match")

        if rgb:
            self.rgb = self.validate_rgb(rgb)
            self.hex = self.toHex(rgb)
        if hex:
            self.hex = self.validate_hex(hex)
            self.rgb = self.toRgb(hex)

    @staticmethod
    def validate_rgb(value) -> tuple[int, int, int] | NoReturn:
        for i in value:
            if i < 0 or i > 255:
                raise ValueError(f"rgb code must contain floats in the range [0, 255]: {value}")
        if len(value) != 3:
            raise ValueError(f"rgb code must contain 3 floats: {value}")
        return value

    @staticmethod
    def validate_hex(value) -> str | NoReturn:
        if value[0] != "#":
            raise ValueError(f"hex must begin with '#': {value}")
        if len(value) != 7:
            raise ValueError(f"hex must contain 7 symbols: {value}")

        alphabet = "1234567890qwertyuiopasdfghjklzxcvbnm"
        for i in value[1:]:
            if i not in alphabet:
                raise ValueError(f"hex must contain 6 digits/chars after the '#': {value}, '{i}'")
        return value

    def toHex(self, rgb: tuple[int, int, int] = None) -> str:
        if rgb is None:
            rgb = self.rgb
        return '#%02x%02x%02x' % rgb

    def toRgb(self, hex_value: str = None) -> tuple[int, int, int]:
        if hex_value is None:
            hex_value = self.hex
        hex_value = hex_value.lstrip("#")
        return tuple[int, int, int](int(hex_value[i:i + 2], 16) for i in (0, 2, 4))

    def mix(self, other):
        return type(self)(rgb=(
            (self.rgb[0] + other.rgb[0]) // 2,
            (self.rgb[1] + other.rgb[1]) // 2,
            (self.rgb[2] + other.rgb[2]) // 2
        ))

    def __add__(self, other):
        return self.mix(other)

    def __str__(self):
        return f"RGB: {self.rgb} | HEX: {self.hex} | visible: {self.visible}"


if __name__ == "__main__":
    c1 = Color(hex="#112362")
    c2 = Color(rgb=(12, 255, 75))
    print(f"{c1}")
    print(f"{c2}")
    print(f"{c1 + c2}")
