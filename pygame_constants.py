import pygame
import configparser

config = configparser.ConfigParser()
config.read('game.ini')
FONT = config.get('GAME', 'font')
del config

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM = (255, 253, 209)
PINK = (255, 192, 203)
BLUE = (0, 100, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 95, 31)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
YELLOW = (255, 255, 0)
EMERALD = (2, 138, 15)
GREY = (127, 127, 127)

FONT_COURIER = pygame.font.Font(FONT, 30)
FONT_COURIER_20 = pygame.font.Font(FONT, 20)