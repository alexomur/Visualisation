from classes.Vector2 import Vector2
import math


def angle_vectors(vec1: Vector2, vec2: Vector2, radian=True) -> float:
    if radian:
        return math.acos((vec1*vec2)/(vec1.len()*vec2.len()))
    return 180*math.acos((vec1*vec2)/(vec1.len()*vec2.len()))/math.pi
