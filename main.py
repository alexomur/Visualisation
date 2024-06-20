from modules import math
from classes.Vector2 import Vector2

def main():
    print(
        math.angle_vectors(
            Vector2(-1, 0),
            Vector2(1, 0),
            False
        )
    )


if __name__ == "__main__":
    main()