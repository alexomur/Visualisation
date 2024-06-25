from pydantic import BaseModel


# TODO: finish the Color class using BaseModel
class Color(BaseModel):
    rgb: tuple[float, float, float]
    hex: str

