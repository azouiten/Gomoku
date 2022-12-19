import pygame

class GameSurface:
    """
    This class is an abstraction of a pygame surface.
    """
    def __init__(self, main_surface=False, dims=(1200, 800)):
        self._width, self._height = dims

        if main_surface:
            pygame.init()
            self._surface = pygame.display.set_mode((self.width, self.height))
        else:
            self._surface = pygame.Surface((self.width, self.height))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def surface(self):
        return self._surface

class Window(GameSurface):
    """ 
    This class represents the surface of the window
    where every thing is drawn.
    """
    def __init__(self):
        super().__init__(main_surface=True)

class Board(GameSurface):
    """ 
    This class represents the surface of the board.
    """
    def __init__(self):
        super().__init__()

class Setup(GameSurface):
    """ 
    This class represents the surface of the setup 
    state of the game.
    """
    def __init__(self):
        super().__init__()

class Final(GameSurface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """
    def __init__(self):
        super().__init__()

class Game:
    """
    This class represents the game logic.
    """
    def __init__(self):
        self._window = Window()
        self._setup = Setup()
        self._board = Board()
        self._final = Final()
        self.repeat = True


    @property
    def window(self):
        return self._window

    @property
    def setup(self):
        return self._setup

    @property
    def board(self):
        return self._board

    @property
    def final(self):
        return self._final

    def loop(self):
        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.repeat = False

    def run(self):
        self.loop()
