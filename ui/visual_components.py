import pygame
from surface import Surface
from fonts import *

BOARD_COLOR = pygame.Color("#EAE6E3")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")
BLUE = pygame.Color("#0000ff")

class Button(Surface):
    """
    Class representing an interactive button object
    """
    def __init__(self, cx: int, cy: int, fg: str, bg: str, text: str, font, disabled=False, interactive=True):

        # Load font
        self._font = font

        self._bg_str = bg
        self._fg_str = fg
        self._bg = pygame.Color(bg)
        self._fg = pygame.Color(fg)
        self._bg_hov = pygame.Color(bg)
        self._bg_hov.r = self.bg.r - 30 if self.bg.r >= 30 else self.bg.r
        self._bg_hov.b = self.bg.b - 30 if self.bg.b >= 30 else self.bg.b
        self._bg_hov.g = self.bg.g - 30 if self.bg.g >= 30 else self.bg.g

        self._cx = cx
        self._cy = cy

        self._orig_text = text
        self._text = self.font.render(text, True, pygame.Color(self.fg), pygame.Color(self.bg))

        self.surf_width = self.text.get_width()
        self.surf_height = self.text.get_height()

        super().__init__(self.surf_width + 100, self.surf_height + 50, None)
        self.rect.center = (self._cx, self._cy)
        self._text_rect = self.text.get_rect()
        self._text_rect.center = (int(self.width / 2), int(self.height / 2))

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


class CheckBoxs(Surface):

    def __init__(self, position, pairs):
        self._container = []

        # Create instances of CheckBox and set containers' max height accordingly
        offset = 0
        for key in pairs.keys():
            new_position = (position[0] + offset + 1 + 100, position[1])
            self._container.append(CheckBox(pairs[key], key, offset, new_position))
            offset = offset + self._container[-1].height + 1

        # Set max width of the container
        total_width = 0
        for checkbox in self._container:
            total_width = checkbox.width if checkbox.width > total_width else total_width

        # Anchor to first element of container list or set to None
        self._anchor = self._container[0]
        self._anchor.checked = True
        super().__init__(total_width, offset, (position[0]+100, position[1]))
        self.rect.top += 100

    @property
    def container(self):
        return self._container

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value

    def update(self):
        self.surface.fill(BOARD_COLOR)

        # Set the new checkbox
        for box in self.container:
            box.update()
            if box.checked and box is not self.anchor:
                self.anchor.checked = False
                self.anchor = box
                box.checked = True
            self.surface.blit(box.surface, box.rect)
        

class CheckBox(Surface):
    __slots__ = ('_label', '_box', '_value', '_filler', '_checked', '_label_rect', '_hovered')

    def __init__(self, label, value, offset, position):
        self._label = h3_t.render(label, True, BLACK, BOARD_COLOR)
        self._label_rect = self.label.get_rect()
        self._label_rect.top = 5
        self._label_rect.left = 70

        self._value = value

        self._box = Surface(40, 40, None)
        self._box.rect.top = 5

        self._filler = Surface(30, 30, None)
        self._filler.surface.fill(WHITE)
        self._filler.rect.top = 10
        self._filler.rect.left = 5

        self._checked = False
        self._hovered = False

        super().__init__(
            self._label.get_width() + 70, 
            50 if self._label.get_height() < 50 else self._label.get_height(), 
            position
        )
        self.rect.top += offset

    @property
    def label(self):
        return self._label

    @property
    def label_rect(self):
        return self._label_rect

    @property
    def value(self):
        return self._value

    @property
    def box(self):
        return self._box

    @property
    def filler(self):
        return self._filler

    @property
    def checked(self):
        return self._checked

    def check_hover(self):
        x, y = pygame.mouse.get_pos()
        self.hovered = False
        if x >= self.position[1] and x <= self.position[1] + self.width:
            if y >= self.position[0] and y <= self.position[0] + self.height:
                self.hovered = True
        return self.hovered

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, value):
        self._hovered = value

    @checked.setter
    def checked(self, value):
        self._checked = value

    def check_clicked(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.position[1] and x <= self.position[1] + self.width:
            if y >= self.position[0] and y <= self.position[0] + self.height:
                self.checked = True

    def update(self):
        self.surface.fill(BOARD_COLOR)
        self.surface.blit(self.box.surface, self.box.rect)
        self.check_hover()
        if self.checked or self.hovered:
            self.surface.blit(self.filler.surface, self.filler.rect)
        self.surface.blit(self.label, self._label_rect)
