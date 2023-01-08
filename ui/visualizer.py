import pygame
from surface    import Surface
from fonts      import *
from init       import *
from random     import randint
from computer   import Computer
from setup      import Setup
from board      import Board
from final      import Final


# Setup relevant variables
QUIT = False
HEIGHT = 800
WIDTH  = 1400
BOARD_COLOR = pygame.Color("#EAE6E3")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")


# Initialize pygame
pygame.init()


class State:
    """
    This class represents a board state read from the game logic.
    """

    __slots__ = ('_state',)

    def __init__(self):
        self._state = [[str(randint(0, 2)) for j in range(19)] for i in range(19)]

    def __getitem__(self, index):
        return self.state[index]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def update(self, x, y, player):
        self[y][x] = player


class Window:
    """
    This class represents the display surface.
    """

    __slots__ = ('_width', '_height', '_surface')

    def __init__(self):
        self._width   = WIDTH
        self._height  = HEIGHT
        self._surface = pygame.display.set_mode((self._width, self._height))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def surface(self):
        return self._surface

    def blit(self, surface: Surface):
        self._surface.blit(surface.surface, (0, 0))

    def update(self):
        pygame.display.flip()


class Game:
    """
    This class represents the game logic.
    """

    __slots__ = ('_state', '_window', '_setup_surface', '_board_surface', '_final_surface', '_current_surface', '_computer')

    def __init__(self):
        self._state           = State()
        self._window          = Window()
        self._setup_surface   = Setup(self._window)
        self._board_surface   = Board(self._window, 1, self._state, self._setup_surface)
        self._final_surface   = Final(self._window)
        self._current_surface = FINAL_SURFACE

    @property
    def window(self):
        return self._window

    @property
    def setup_surface(self):
        return self._setup_surface

    @property
    def board_surface(self):
        return self._board_surface

    @property
    def final_surface(self):
        return self._final_surface

    @property
    def current_surface(self):
        return self._current_surface

    @current_surface.setter
    def current_surface(self, value):
        self._current_surface = value

    @property
    def state(self):
        return self._state

    def run(self):
        global QUIT

        while not QUIT:
            if self.current_surface == SETUP_SURFACE:
                self.current_surface = self.setup_surface.loop()
            elif self.current_surface == BOARD_SURFACE:
                self.current_surface = self.board_surface.loop()
            elif self.current_surface == FINAL_SURFACE:
                self.current_surface = self.final_surface.loop()


if __name__ == "__main__":
    game = Game()
    game.run()

# [ ] Link the setup with the board
# [ ] Kill the bot(computer) process at the end
