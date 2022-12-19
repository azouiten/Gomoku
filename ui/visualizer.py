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
