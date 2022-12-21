import pygame

class Surface:
    """
    This class is an abstraction of a pygame surface.
    """
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._surface = pygame.Surface((self._width, self._height))
        self._rect = self.surface.get_rect()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def surface(self):
        return self._surface

    @property
    def rect(self):
        return self._rect