import pygame

class Surface:
    """
    This class is an abstraction of a pygame surface.
    """
    __slots__ = ('_position', '_width', '_height', '_surface', '_rect')

    def __init__(self, width, height, position):
        self._position = position
        self._width = width
        self._height = height
        self._surface = pygame.Surface((self._width, self._height))
        self._rect = self.surface.get_rect()

    @property
    def position(self):
        return self._position

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