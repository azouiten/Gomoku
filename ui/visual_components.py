import pygame
from surface import Surface
from fonts import *

BOARD_COLOR = pygame.Color("#EAE6E3")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")

class Button(Surface):
    """
    Class representing an interactive button object
    """
    def __init__(self, cx: int, cy: int, fg: str, bg: str, text: str, font, position, disabled=False, interactive=True):

        # Load font
        self._font = font

        self._bg_str = bg
        self._fg_str = fg
        self._bg = pygame.Color(bg)
        self._fg = pygame.Color(fg)
        self._bg_hov = pygame.Color(bg)
        self._bg_hov.r = self.bg.r - 30 if self.bg.r >= 30 else self.bg.r
        self._bg_hov.b = self.bg.b - 30 if self.bg.b >= 30 else self.bg.b
        self._bg_hov.g = self.bg.g - 30 if self.bg.b >= 30 else self.bg.b

        self._cx = cx
        self._cy = cy

        self._orig_text = text
        self._text = self.font.render(text, True, pygame.Color(self.fg), pygame.Color(self.bg))

        self.surf_width = self.text.get_width()
        self.surf_height = self.text.get_height()

        super().__init__(self.surf_width + 100, self.surf_height + 50)
        self.rect.center = (self._cx, self._cy)
        self._text_rect = self.text.get_rect()
        self._text_rect.center = self.rect.center

        self._hover = False
        self._disabled = disabled
        self._interactive = interactive
        self._pressed = False


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
        self.bg = self._bg_hov
        self.text = self.font.render(self.orig_text, True, pygame.Color(self.fg), pygame.Color(self.bg))

    @property
    def hover(self):
        return self._hover

    @hover.setter
    def hover(self, value):
        self._hover = value

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value

    @property
    def interactive(self):
        return self._interactive

    def set_hover(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.cx - int(self.width / 2) and x <= self.cx + int(self.width / 2):
            if y >= self.cy - int(self.height / 2) and y <= self.cy + int(self.height / 2):
                self.bg = pygame.Color(self.bg_str) if self.pressed else self._bg_hov
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
                if self.interactive:
                    self.bg = pygame.Color(self.bg_str) if self.pressed else self._bg_hov
                    self.pressed = not self.pressed
                return True
        return False

    def update(self):
        if not self.disabled:
            self.set_hover()
        else:
            self.disable()
        self.surface.fill(self.bg)
        self.surface.blit(self.text, self.text_rect)


class PlayerMenu(Surface):
    """
    This class represents a drop down menu
    """

    # Player type
    HUMAN = 0
    BOT = 1

    # Bot accuracy
    LBOSS = 0
    KAYL3AB = 1
    MKALAKH = 2

    def __init__(self, width, height, player_type=0):
        super().__init__(width, height)

        self._player = player_type
        self._selected = self._player
        self._depth = PlayerMenu.MKALAKH
        self._human_button = Button(self.rect.left+200, self.rect.top+50, "#000000", "#F5BB55", "Human", h3_t, False, True)
        # self._bot_button   = Button(self.width / 2, self.height / 2 + 200, "#EAE6E3", "#000000", "Bot", h3_t)
        # self._type_surface = Surface(width, 100)


    @property
    def type_surface(self):
        return self._type_surface

    @property
    def human_button(self):
        return self._human_button

    def update(self):
        self.surface.fill(BOARD_COLOR)
        self.human_button.update()
        self.surface.blit(self._human_button.surface, self._human_button.rect)