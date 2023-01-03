import pygame
import math
from surface import Surface
from visual_components import Button, CheckBox, CheckBoxs
from fonts import *
import subprocess
from pygame import gfxdraw
from random import randint

# Setup relevant variables
QUIT = False
HEIGHT = 800
WIDTH  = 1400
BOARD_COLOR = pygame.Color("#EAE6E3")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")


def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius+1, BLACK)
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


# Initialize pygame
pygame.init()


class DataInterface:
    """
    This class represents the medium of data transfer between the visualizer
    and the gomoku executable.
    """
    def __init__(self, target=None):
        self._process = subprocess.Popen('')
    
    @property
    def process(self):
        return self._process

    def create_outward_pip(self):
        pass


class State:
    """
    This class represents a board state read from the game logic.
    """
    __slots__ = ('_state',)
    def __init__(self):
        self._state = [[str(randint(0, 2)) for j in range(19)] for i in range(19)]

    def __getitem__(self, index):
        return self.state[index]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def update(self, x, y, player):
        self[y][x] = player

class Window:
    """
    This class represents the display surface.
    """
    def __init__(self):
        self._width   = WIDTH
        self._height  = HEIGHT
        self._surface = pygame.display.set_mode((self._width, self._height))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def surface(self):
        return self._surface

    def blit(self, surface: Surface):
        self._surface.blit(surface.surface, (0, 0))

    def update(self):
        pygame.display.flip()


class Setup(Surface):
    """ 
    This class represents the setup surface
    """

    HUMAN    = 1
    COMPUTER = 2

    EASY   = 1
    MEDIUM = 2
    HARD   = 3

    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._window = window
        self.repeat = True

        self._start = Button(150, 100, "#000000", "#66F587", "START", h3_t)

        # Player 1 setup surface
        self._p1_surf = Surface(600, 600, (150, 100))
        self._p1_surf.rect.top = 150
        self._p1_surf.rect.left = 100

        self._p1_type = CheckBoxs(
            (150, 100), 
            {Setup.HUMAN: 'Human', Setup.COMPUTER: 'Computer'}
        )
        self._p1_type.rect.top = 100
        self._p1_type.rect.left = 0

        self._p1_mode = CheckBoxs(
            (300, 100), 
            {Setup.EASY: 'Easy', Setup.MEDIUM: 'Medium', Setup.HARD: 'Hard'}
        )
        self._p1_mode.rect.top = 250
        self._p1_mode.rect.left = 0

        # Player 2 setup surface

        self._p2_surf = Surface(600, 600, (150, 100))
        self._p2_surf.rect.top = 150
        self._p2_surf.rect.left = 600

        self._p2_type = CheckBoxs(
            (150, 600), 
            {Setup.HUMAN: 'Human', Setup.COMPUTER: 'Computer'}
        )
        self._p2_type.rect.top = 100
        self._p2_type.rect.left = 0

        self._p2_mode = CheckBoxs(
            (300, 600), 
            {Setup.EASY: 'Easy', Setup.MEDIUM: 'Medium', Setup.HARD: 'Hard'}
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

    def draw_box_1(self):
        header = h3_t.render('Player 1', True, BLACK, BOARD_COLOR)
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
        header = h3_t.render('Player 2', True, BLACK, BOARD_COLOR)
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
        middle = h2_t.render('Game Setup', True, BLACK, BOARD_COLOR)
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
                        return Game.BOARD
                    for box in type_checkboxs:
                        box.check_clicked()
                    for box in mode_checkboxs:
                        box.check_clicked()

            self.start.update()
            self.surface.blit(self.start.surface, self.start.rect)
            self.draw_box_1()
            self.draw_box_2()
            self.window.blit(self)
            pygame.display.update()


class Board(Surface):
    """ 
    This class represents the board surface (game board + sidebar).
    """
    __slots__ = ('_player', '_board', '_sidebar', '_state', '_window', '_repeat', '_offset', '_limit', '_step', '_linspace')
    def __init__(self, window, player, initial_state):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._player  = player
        self._board   = Surface(HEIGHT, HEIGHT, None)
        self._sidebar = Surface(WIDTH-HEIGHT, HEIGHT, None)
        self._state   = initial_state
        self._window  = window
        self._repeat   = True
        self._offset   = 40
        self._limit    = self.board.height - self.offset * 2 - 18
        self._step     = int(self.limit / 18)
        self._linspace = [i+self.step for i in range(0, self.board.width - self.offset, self.step)]

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
                    draw_circle(self.board.surface, x, y, 16, pygame.Color(color))

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
        draw_circle(self.board.surface, x, y, radius, pygame.Color(color))
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
                    print(x, y, self.state.state[y][x])
                    if self.state.state[y][x] == '0':
                        self.state.update(x, y, str(self.player))
                        self.player = 1 if self.player == 2 else 2
            if not QUIT:
                self.update()


class Final(Surface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """
    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._repeat = True
        self._window = window
        self._winner = 2
        self._button = Button(self.width / 2, self.height / 2 + 200, "#000000", "#F5BB55", "REMATCH", h3_t)

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
        header = h2_b.render('Game Finished!', True, BLACK, BOARD_COLOR)
        header_rect = header.get_rect()
        header_rect.center = (self.width / 2, self.height / 2 - 100)

        # Mid-screen message
        if self.winner == 0:
            middle = h3_r.render('The game is a Tie', True, BLACK, BOARD_COLOR)
        else:
            middle = h3_r.render(f'Player {self.winner} is Victorious', True, BLACK, BOARD_COLOR)
        middle_rect = middle.get_rect()
        middle_rect.center = (self.width / 2, self.height / 2)

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
                        return Game.SETUP

            self.button.update()
            self.surface.blit(self.button.surface, self.button.rect)
            self.window.blit(self)
            pygame.display.update()


class Game:
    """
    This class represents the game logic.
    """

    SETUP = 1
    BOARD = 2
    FINAL = 3

    def __init__(self):
        self._state         = State()
        self._window        = Window()
        self._setup_surface = Setup(self._window)
        self._board_surface = Board(self._window, 1, self._state)
        self._final_surface = Final(self._window)
        self._current_surface = Game.FINAL

    @property
    def window(self):
        return self._window

    @property
    def setup_surface(self):
        return self._setup_surface

    @property
    def board_surface(self):
        return self._board_surface

    @property
    def final_surface(self):
        return self._final_surface

    @property
    def current_surface(self):
        return self._current_surface

    @current_surface.setter
    def current_surface(self, value):
        self._current_surface = value

    @property
    def state(self):
        return self._state

    def run(self):
        global QUIT

        while not QUIT:
            if self.current_surface == Game.SETUP:
                self.current_surface = self.setup_surface.loop()
            elif self.current_surface == Game.BOARD:
                self.current_surface = self.board_surface.loop()
            elif self.current_surface == Game.FINAL:
                self.current_surface = self.final_surface.loop()


if __name__ == "__main__":
    game = Game()
    game.run()

