import fonts
from surface import Surface
from visual_components import Button, CheckBoxs
from init import *


class Setup(Surface):
    """ 
    This class represents the setup surface
    """

    __slots__ = ('_window', '_repeat', '_start', '_p1_surf', '_p1_type', '_p1_mode', '_p2_surf', '_p2_type', '_p2_mode')

    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._window = window
        self._repeat = True

        self._start = Button(150, 100, "#000000", "#66F587", "START", fonts.h3_t)

        # Player 1 setup surface
        self._p1_surf = Surface(600, 600, (150, 100))
        self._p1_surf.rect.top = 150
        self._p1_surf.rect.left = 100

        self._p1_type = CheckBoxs(
            (150, 100), 
            {
                HUMAN: 'Human', 
                COMPUTER: 'Computer'
            }
        )
        self._p1_type.rect.top = 100
        self._p1_type.rect.left = 0

        self._p1_mode = CheckBoxs(
            (300, 100), 
            {
                EASY: 'Easy', 
                MEDIUM: 'Medium', 
                HARD: 'Hard'
            }
        )
        self._p1_mode.rect.top = 250
        self._p1_mode.rect.left = 0

        # Player 2 setup surface

        self._p2_surf = Surface(600, 600, (150, 100))
        self._p2_surf.rect.top = 150
        self._p2_surf.rect.left = 600

        self._p2_type = CheckBoxs(
            (150, 600), 
            {
                HUMAN: 'Human', 
                COMPUTER: 'Computer'
            }
        )
        self._p2_type.rect.top = 100
        self._p2_type.rect.left = 0

        self._p2_mode = CheckBoxs(
            (300, 600), 
            {
                EASY: 'Easy', 
                MEDIUM: 'Medium', 
                HARD: 'Hard'
            }
        )
        self._p2_mode.rect.top = 250
        self._p2_mode.rect.left = 0
        
    @property
    def window(self):
        return self._window

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def p1_surf(self):
        return self._p1_surf

    @property
    def p1_type(self):
        return self._p1_type

    @property
    def p1_mode(self):
        return self._p1_mode

    @property
    def p2_surf(self):
        return self._p2_surf

    @property
    def p2_type(self):
        return self._p2_type

    @property
    def p2_mode(self):
        return self._p2_mode

    @property
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        self._repeat = value

    def draw_box_1(self):
        header = fonts.h3_t.render('Player 1', True, BLACK_COLOR, BOARD_COLOR)
        header_rect = header.get_rect()
        header_rect.center = (100, 60)

        self.p1_surf.surface.fill(BOARD_COLOR)
        self.p1_surf.surface.blit(header, header_rect)

        # Update type checkboxs
        self.p1_type.update()
        self.p1_surf.surface.blit(self.p1_type.surface, self.p1_type.rect)

        # Blit mode surface
        if self.p1_type.anchor.value == 2:
            self.p1_mode.update()
            self.p1_surf.surface.blit(self.p1_mode.surface, self.p1_mode.rect)

        # Blit first player surface on the window
        self.surface.blit(self.p1_surf.surface, self.p1_surf.rect)

    def draw_box_2(self):
        header = fonts.h3_t.render('Player 2', True, BLACK_COLOR, BOARD_COLOR)
        header_rect = header.get_rect()
        header_rect.center = (100, 60)

        self.p2_surf.surface.fill(BOARD_COLOR)
        self.p2_surf.surface.blit(header, header_rect)

        # Update type checkboxs
        self.p2_type.update()
        self.p2_surf.surface.blit(self.p2_type.surface, self.p2_type.rect)

        # Blit mode surface
        if self.p2_type.anchor.value == 2:
            self.p2_mode.update()
            self.p2_surf.surface.blit(self.p2_mode.surface, self.p2_mode.rect)

        # Blit first player surface on the window
        self.surface.blit(self.p2_surf.surface, self.p2_surf.rect)

    def loop(self):
        global QUIT

        # subtitle
        middle = fonts.h2_t.render('Game Setup', True, BLACK_COLOR, BOARD_COLOR)
        middle_rect = middle.get_rect()
        middle_rect.center = (self.width / 2, 70)

        self.surface.fill(BOARD_COLOR)
        self.surface.blit(middle, middle_rect)

        type_checkboxs = [*self.p1_type.container, *self.p2_type.container]
        mode_checkboxs = [*self.p1_mode.container, *self.p2_mode.container]

        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.start.clicked():
                        return BOARD_SURFACE
                    for box in type_checkboxs:
                        box.check_clicked()
                    for box in mode_checkboxs:
                        box.check_clicked()

            self.start.update()
            self.surface.blit(self.start.surface, self.start.rect)
            self.draw_box_1()
            self.draw_box_2()
            self.window.blit(self)
            self.window.update()
            CLOCK.tick(30)
