import pygame
import math
from surface import Surface
from visual_components import Button, CheckBox, CheckBoxs
from fonts import *
import subprocess
from pygame import gfxdraw

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
    def __init__(self):
        self._state = None

    @property
    def state(self):
        return self._state


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


class Board(Surface):
    """ 
    This class represents the board surface (game board + sidebar).
    """
    def __init__(self, window, player, initial_state):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self._player  = player
        self._board   = Surface(HEIGHT, HEIGHT, None)
        self._sidebar = Surface(WIDTH-HEIGHT, HEIGHT, None)
        self._state   = initial_state
        self._window  = window
        self.repeat   = True
        self.offset   = 40
        self.limit    = self.board.height - self.offset * 2 - 18
        self.step     = int(self.limit / 18)
        self.linspace = [i+self.step for i in range(0, self.board.width - self.offset, self.step)]

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
    def window(self):
        return self._window

    def draw_board(self):
        if self.check_hover():
            BLUE = pygame.Color("#0000ff")
            self.board.surface.fill(BLUE)
        else:
            self.board.surface.fill(BOARD_COLOR)
        for i in range(0, 19):
            thickness = 2 if i in (0, 3, 9, 15, 18) else 1

            # Draw horizontal lines
            xs = self.offset + 0
            ys = self.offset + i * self.step
            xe = self.offset + self.limit
            ye = self.offset + i * self.step
            pygame.draw.line(self.board.surface, pygame.Color('#000000'), (xs, ys), (xe, ye), thickness)

            # Draw vertical lines
            xs = self.offset + i * self.step
            ys = self.offset + 0
            xe = self.offset + i * self.step
            ye = self.offset + self.limit
            pygame.draw.line(self.board.surface, pygame.Color('#000000'), (xs, ys), (xe, ye), thickness)
        
    def update_board(self):
        self.draw_board()
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

    def check_hover(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.offset and x <= self.limit + self.offset:
            if y >= self.offset and y <= self.limit + self.offset:
                return True
        return False

    def show_hover(self):
        x, y = pygame.mouse.get_pos()
        color = "#ffffff" if self.player == 1 else "#000000"
        nx = self.linspace[math.floor((x-20) / self.step)]
        ny = self.linspace[math.floor((y-20) / self.step)]
        if math.sqrt((x-nx)**2 + (y-ny)**2) <= 25:
            x, y = nx, ny
        draw_circle(self.board.surface, x, y, 18, pygame.Color(color))
        return x, y

    def loop(self):
        global QUIT

        self.update()
        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
                if event.type == pygame.MOUSEBUTTONUP and self.check_hover():
                    self.player = 1 if self.player == 2 else 2
            self.update()


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

        self._p1_surf = Surface(600, 600, (150, 100))
        self._p1_surf.rect.top = 150
        self._p1_surf.rect.left = 100

        self._p1_cb = CheckBoxs(
            self._p1_surf.position, 
            {1: 'Computer', 2: 'Human'}
        )
        
    @property
    def window(self):
        return self._window

    @property
    def p1_surf(self):
        return self._p1_surf

    # @property
    # def p2_surf(self):
    #     return self._p2_surf

    @property
    def p1_cb(self):
        return self._p1_cb

    def draw_box_1(self):
        header = h3_t.render('Player 1', True, BLACK, BOARD_COLOR)
        header_rect = header.get_rect()
        header_rect.center = (140, self.p1_surf.rect.center[1] / 2 - 250)

        self.p1_surf.surface.fill(BOARD_COLOR)
        self.p1_surf.surface.blit(header, header_rect)

        self.p1_cb.update()
        self.p1_surf.surface.blit(self.p1_cb.surface, self.p1_cb.rect)
        self.surface.blit(self.p1_surf.surface, self.p1_surf.rect)

    def loop(self):
        global QUIT

        # subtitle
        middle = h2_t.render('Game Setup', True, BLACK, BOARD_COLOR)
        middle_rect = middle.get_rect()
        middle_rect.center = (self.width / 2, 70)

        self.surface.fill(BOARD_COLOR)
        self.surface.blit(middle, middle_rect)

        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
                if event.type == pygame.MOUSEBUTTONUP:
                    for box in self.p1_cb.container:
                        box.check_clicked()

            self.draw_box_1()
            self.window.blit(self)
            pygame.display.update()


class Final(Surface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """
    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT, (0, 0))
        self.repeat = True
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
                        return 1

            self.button.update()
            self.surface.blit(self.button.surface, self.button.rect)
            self.window.blit(self)
            pygame.display.update()


class Game:
    """
    This class represents the game logic.
    """
    def __init__(self):
        self.repeat         = True
        self._state         = State()
        self._window        = Window()
        self._setup_surface = Setup(self._window)
        self._board_surface = Board(self._window, 1, self._state)
        self._final_surface = Final(self._window)
        self._current_surface = 2


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
            if self.current_surface == 1:
                self.current_surface = self.setup_surface.loop()
            elif self.current_surface == 2:
                self.current_surface = self.board_surface.loop()
            elif self.current_surface == 3:
                self.current_surface = self.final_surface.loop()


if __name__ == "__main__":
    game = Game()
    game.run()

