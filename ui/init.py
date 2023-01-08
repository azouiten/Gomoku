import pygame

# Clock tick: 30 ticks
CLOCK = pygame.time.Clock()

# Current surface
SETUP_SURFACE = 1
BOARD_SURFACE = 2
FINAL_SURFACE = 3

# Quit variable
QUIT        = False

# Constants
HEIGHT      = 800
WIDTH       = 1400
BOARD_COLOR = pygame.Color("#EAE6E3")
WHITE_COLOR = pygame.Color("#ffffff")
BLACK_COLOR = pygame.Color("#000000")

# Player type
HUMAN       = 1
COMPUTER    = 2

# Computer difficulty
EASY        = 1
MEDIUM      = 2
HARD        = 3

# Path to the executable
EXE_PATH = '../src/a.out'