import math
from pygame import gfxdraw
from surface import Surface
from init import *
from computer import Computer

class Board(Surface):
    """ 
    This class represents the board surface (game board + sidebar).
    """

    __slots__ = ('_player', '_board', '_sidebar', '_state', '_window', '_repeat', '_offset', '_limit', '_step', '_linspace', '_setup', '_p1', '_p2')

    def __init__(self, window, player, initial_state, setup):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._player   = player
        self._board    = Surface(HEIGHT, HEIGHT, None)
        self._sidebar  = Surface(WIDTH-HEIGHT, HEIGHT, None)
        self._state    = initial_state
        self._window   = window
        self._repeat   = True
        self._offset   = 40
        self._limit    = self.board.height - self.offset * 2 - 18
        self._step     = int(self.limit / 18)
        self._linspace = [i+self.step for i in range(0, self.board.width - self.offset, self.step)]
        self._setup    = setup
        self._p1       = None
        self._p2       = None

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @p1.setter
    def p1(self, value):
        self._p1 = value

    @p2.setter
    def p2(self, value):
        self._p2 = value

    @property
    def setup(self):
        return self._setup

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def board(self):
        return self._board

    @property
    def sidebar(self):
        return self._sidebar

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        self._repeat = value

    @property
    def offset(self):
        return self._offset

    @property
    def limit(self):
        return self._limit

    @property
    def step(self):
        return self._step

    @property
    def linspace(self):
        return self._linspace

    @property
    def window(self):
        return self._window

    @staticmethod
    def draw_circle(surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius+1, BLACK_COLOR)
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def draw_board(self):
        self.board.surface.fill(BOARD_COLOR)

        for i in range(0, 19):
            # Draw horizontal lines
            xs = self.offset + 0
            ys = self.offset + i * self.step
            xe = self.offset + self.limit
            ye = self.offset + i * self.step
            pygame.draw.line(self.board.surface, pygame.Color('#000000'), (xs, ys), (xe, ye), 1)

            # Draw vertical lines
            xs = self.offset + i * self.step
            ys = self.offset + 0
            xe = self.offset + i * self.step
            ye = self.offset + self.limit
            pygame.draw.line(self.board.surface, pygame.Color('#000000'), (xs, ys), (xe, ye), 1)

    def draw_state(self):
        for r, row in enumerate(self.state.state):
            for c, col in enumerate(row):
                if col in ['1', '2']:
                    color = "#ffffff" if col == '1' else "#000000"
                    x = self.linspace[c] + 1
                    y = self.linspace[r] + 1
                    Board.draw_circle(self.board.surface, x, y, 16, pygame.Color(color))

    def check_hover(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.offset and x <= self.limit + self.offset:
            if y >= self.offset and y <= self.limit + self.offset:
                return True
        return False

    def show_hover(self):
        radius = 20
        x, y = pygame.mouse.get_pos()
        color = "#ffffff" if self.player == 1 else "#000000"
        nx = self.linspace[math.floor((x-radius) / self.step)]
        ny = self.linspace[math.floor((y-radius) / self.step)]
        if math.sqrt((x-nx)**2 + (y-ny)**2) <= 25:
            x, y = nx + 1, ny + 1
        Board.draw_circle(self.board.surface, x, y, radius, pygame.Color(color))
        return x, y

    def update_board(self):
        self.draw_board()
        self.draw_state()
        if self.check_hover():
            self.show_hover()
        self.surface.blit(self.board.surface, (0, 0))

    def update_sidebar(self):
        self.sidebar.surface.fill(pygame.Color("#EAE6E3"))
        self.surface.blit(self.sidebar.surface, (self.board.width, 0))

    def update(self):
        self.update_board()
        self.update_sidebar()
        self.window.blit(self)
        self.window.update()

    def loop(self):
        global QUIT

        if self.setup.p1_type.anchor.value == COMPUTER:
            if self.p1:
                self.p1.stop()
            self.p1 = Computer()
            self.p1.start()
            print('Created p1:', self.p1.process)
        if self.setup.p2_type.anchor.value == COMPUTER:
            if self.p2:
                self.p2.stop()
            self.p2 = Computer()
            self.p2.start()
            print('Created p2')

        print('p1', self.setup.p1_type.anchor.value)
        print('p2', self.setup.p2_type.anchor.value)
        
        self.update()
        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.check_hover():
                    x, y = pygame.mouse.get_pos()
                    x = math.floor((x-16) / self.step)
                    y = math.floor((y-16) / self.step)
                    if self.state.state[y][x] == '0':
                        self.state.update(x, y, str(self.player))
                        self.player = 1 if self.player == 2 else 2
            if not QUIT:
                self.update()
            CLOCK.tick(30)

        # # Reset the players: Need to check if the player is comuter to close it's process
        # self.p1 = None
        # self.p2 = None