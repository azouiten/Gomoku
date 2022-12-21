import pygame
from surface import Surface
from button import Button


# Setup relevant variables and informations
QUIT = False
HEIGHT = 1000
WIDTH  = 1500
BOARD_COLOR = pygame.Color("#E6C475")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")


# Initialize pygame
pygame.init()

# Load fonts
font_B = pygame.font.Font('./ressources/fonts/ChivoMono-Bold.ttf', 56)
font_R = pygame.font.Font('./ressources/fonts/ChivoMono-Regular.ttf', 56)
font_T = pygame.font.Font('./ressources/fonts/ChivoMono-Thin.ttf', 56)


class State:
    """
    This class represents a board state read from the game logic.
    """
    def __init__(self):
        self._state = None

    @property
    def state(self):
        return self._state


class Window:
    """ 
    This class represents the display surface.
    """
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


class Board(Surface):
    """ 
    This class represents the board surface (game board + sidebar).
    """
    def __init__(self, player, initial_state):
        super().__init__(WIDTH, HEIGHT)
        self._offset  = 25
        self._player  = player
        self._board   = Surface(HEIGHT - self._offset*2, HEIGHT - self._offset*2)
        self._sidebar = Surface(WIDTH-HEIGHT, HEIGHT)
        self._state   = initial_state
        self._image   = pygame.image.load('./go-board.png')
        self._image   = pygame.transform.scale(self._image, (self._board.height+5, self.board.height+5))

    @property
    def player(self):
        return self._player

    @property
    def board(self):
        return self._board

    @property
    def sidebar(self):
        return self._sidebar
        
    def update_board(self):
        self.board.surface.fill(pygame.Color("#E6C475"))
        self.board.surface.blit(self._image, (-2, -2))
        self.surface.blit(self.board.surface, (self._offset, self._offset))

    def update_sidebar(self):
        self.sidebar.surface.fill(pygame.Color("#EAE6E3"))
        self.surface.blit(self.sidebar.surface, (self.board.width, 0))

    def update(self):
        self.update_board()
        self.update_sidebar()


class Setup(Surface):
    """ 
    This class represents the setup surface
    """
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)


class Final(Surface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)


class Game:
    """
    This class represents the game logic.
    """
    def __init__(self):
        self.repeat         = True
        self._state         = State()
        self._window        = Window()
        self._setup_surface = Setup()
        self._board_surface = Board(1, self._state)
        self._final_surface = Final()


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
    def state(self):
        return self._state

    def loop(self):
        while self.repeat:

            # read event and update relevant informations accordingly.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.repeat = False

            self.board_surface.update()
            self.window.blit(self.board_surface)
            pygame.display.update()

    def run(self):
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.run()

