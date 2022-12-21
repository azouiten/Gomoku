import pygame
from surface import Surface
from fonts import *

WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")

class Button(Surface):
    """
    Class representing an interactive button object
    """
    __slots__ = ('_cx', '_cy', '_bg', '_fg', '_text', '_text_rect', '_hover')

    def __init__(self, cx: int, cy: int, fg: str, bg: str, text: str, font, disabled=False):
        super().__init__(300, 80)

        # Load font
        self._font = font

        self._cx = cx
        self._cy = cy
        self._bg = pygame.Color(bg)
        self._fg = pygame.Color(fg)
        self._bg_str = bg
        self._fg_str = fg
        self._orig_text = text
        self._text = self.font.render(text, True, pygame.Color(self.fg), pygame.Color(self.bg))
        self._text_rect = self.text.get_rect()
        self._text_rect.center = (self.width / 2, self.height / 2)
        self._hover = False
        self._disabled = disabled
        self.rect.center = (self._cx, self._cy)

    @property
    def cx(self):
        return self._cx

    @property
    def cy(self):
        return self._cy

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value: pygame.Color):
        self._bg = value

    @property
    def fg(self):
        return self._fg

    @property
    def bg_str(self):
        return self._bg_str

    @property
    def fg_str(self):
        return self._fg_str

    @property
    def font(self):
        return self._font

    @property
    def orig_text(self):
        return self._orig_text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_rect(self):
        return self._text_rect

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

    def disable(self):
        self.bg = pygame.Color(self.bg_str)
        self.bg.r = self.bg.r - int(self.bg.r * 0.2)
        self.bg.b = self.bg.b - int(self.bg.b * 0.2)
        self.bg.g = self.bg.g - int(self.bg.g * 0.2)
        self.text = self.font.render(self.orig_text, True, pygame.Color(self.fg), pygame.Color(self.bg))

    @property
    def hover(self):
        return self._hover

    @hover.setter
    def hover(self, value):
        self._hover = value

    def set_hover(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.cx - int(self.width / 2) and x <= self.cx + int(self.width / 2):
            if y >= self.cy - int(self.height / 2) and y <= self.cy + int(self.height / 2):
                self.bg = pygame.Color(self.bg_str)
                self.bg.r = self.bg.r - int(self.bg.r * 0.2)
                self.bg.b = self.bg.b - int(self.bg.b * 0.2)
                self.bg.g = self.bg.g - int(self.bg.g * 0.2)
                self.text = self.font.render(self.orig_text, True, pygame.Color(self.fg), pygame.Color(self.bg))
                return 
        self.bg = pygame.Color(self.bg_str)
        self.text = self.font.render(self.orig_text, True, pygame.Color(self.fg), pygame.Color(self.bg))

    def clicked(self):
        if self.disabled:
            return False
        x, y = pygame.mouse.get_pos()
        if x >= self.cx - int(self.width / 2) and x <= self.cx + int(self.width / 2):
            if y >= self.cy - int(self.height / 2) and y <= self.cy + int(self.height / 2):
                return True
        return False

    def update(self):
        if not self.disabled:
            self.set_hover()
        else:
            self.disable()
        self.surface.fill(self.bg)
        self.surface.blit(self.text, self.text_rect)

        