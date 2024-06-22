from modules import math

from constants import colors
from constants.exit_codes import *
from constants.initialisation import *

from classes.Vector2 import Vector2

from dimensions.meters import Meters

import pygame


def main() -> int:
    pygame.init()
    canvas: pygame.Surface = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Visualisation")
    exit_code: int = KEEP_WORKING

    height: Meters = Meters("5 km")
    print(height)

    """vec: Vector2 = Vector2(0., 0., (1., 1.))
    objects = [vec]

    while exit_code == KEEP_WORKING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_code = WINDOW_CLOSED_REASON
        for obj in objects:
            if type(obj) is Vector2:
                obj.move()
        pygame.display.update()"""
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
