from modules import math

from constants import colors
from constants.exit_codes import *
from constants.initialisation import *

from classes.Vector2 import Vector2
import pygame


def main() -> int:
    pygame.init()
    canvas: pygame.Surface = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Visualisation")
    exit_code: int = KEEP_WORKING

    vec: Vector2 = Vector2(0., 0., (1., 1.))
    while exit_code == KEEP_WORKING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_code = WINDOW_CLOSED_REASON
        pygame.display.update()
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
