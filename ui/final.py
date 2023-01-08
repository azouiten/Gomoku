import fonts
from surface import Surface
from init import *
from visual_components import Button


class Final(Surface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """

    __slots__ = ('_repeat', '_window', '_winner', '_button')

    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._repeat = True
        self._window = window
        self._winner = 2
        self._button = Button(int(self.width / 2), int(self.height / 2) + 200, "#000000", "#F5BB55", "REMATCH", fonts.h3_t)

    @property
    def window(self):
        return self._window

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, player):
        self._winner = player

    @property
    def button(self):
        return self._button

    @property
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        self._repeat = value

    def loop(self):
        global QUIT

        # Header message
        header = fonts.h2_b.render('Game Finished!', True, BLACK_COLOR, BOARD_COLOR)
        header_rect = header.get_rect()
        header_rect.center = (int(self.width / 2), int(self.height / 2) - 100)

        # Mid-screen message
        if self.winner == 0:
            middle = fonts.h3_r.render('The game is a Tie', True, BLACK_COLOR, BOARD_COLOR)
        else:
            middle = fonts.h3_r.render(f'Player {self.winner} is Victorious', True, BLACK_COLOR, BOARD_COLOR)
        middle_rect = middle.get_rect()
        middle_rect.center = (int(self.width / 2), int(self.height / 2))

        # Put text on the surface
        self.surface.fill(BOARD_COLOR)
        self.surface.blit(header, header_rect)
        self.surface.blit(middle, middle_rect)
        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.button.clicked():
                        return SETUP_SURFACE

            self.button.update()
            self.surface.blit(self.button.surface, self.button.rect)
            self.window.blit(self)
            self.window.update()
            CLOCK.tick(30)