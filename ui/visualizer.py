import pygame
from surface import Surface
from button import Button
from fonts import *


# Setup relevant variables and informations
QUIT = False
HEIGHT = 1000
WIDTH  = 1500
BOARD_COLOR = pygame.Color("#E6C475")
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")


# Initialize pygame
pygame.init()


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
        super().__init__(WIDTH, HEIGHT)
        self._offset  = 50
        self._player  = player
        self._board   = Surface(HEIGHT - self._offset*2, HEIGHT - self._offset*2)
        self._sidebar = Surface(WIDTH-HEIGHT, HEIGHT)
        self._state   = initial_state
        self._image   = pygame.image.load('./ressources/images/go-board.png')
        self._image   = pygame.transform.scale(self._image, (self._board.height+5, self.board.height+5))
        self._window  = window
        self.repeat   = True

    @property
    def player(self):
        return self._player

    @property
    def board(self):
        return self._board

    @property
    def sidebar(self):
        return self._sidebar

    @property
    def window(self):
        return self._window
        
    def update_board(self):
        self.board.surface.fill(pygame.Color("#E6C475"))
        self.board.surface.blit(self._image, (-2, -2))
        self.surface.blit(self.board.surface, (self._offset, self._offset))

    def update_sidebar(self):
        self.sidebar.surface.fill(pygame.Color("#EAE6E3"))
        self.surface.blit(self.sidebar.surface, (self.board.width + self._offset * 2, 0))

    def update(self):
        self.update_board()
        self.update_sidebar()
        self.window.blit(self)
        pygame.display.update()

    def loop(self):
        global QUIT

        self.update()
        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
            self.update()


class Setup(Surface):
    """ 
    This class represents the setup surface
    """
    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT)
        self._window = window
        self.repeat = True
        self._player_1 = Surface(600, 500)
        self._player_2 = Surface(600, 500)

    @property
    def window(self):
        return self._window

    @property
    def player_1(self):
        return self._player_1

    @property
    def player_2(self):
        return self._player_2

    def draw_box_1(self):
        self.player_1.rect.center = (self.width / 2 - 350, self.height / 2)

        header = h3_t.render('Player 1', True, pygame.Color('#000000'), pygame.Color("#ffffff"))
        header_rect = header.get_rect()
        header_rect.center = (self.player_1.rect.center[0] / 2, self.player_1.rect.center[1] / 2)
        
        self.player_1.surface.fill(WHITE)
        self.player_1.surface.blit(header, header_rect)
        self.surface.blit(self.player_1.surface, self.player_1.rect)

    def draw_box_2(self):
        self.player_2.rect.center = (self.width / 2 + 350, self.height / 2)

        header = h3_t.render('Player 2', True, pygame.Color('#000000'), pygame.Color("#ffffff"))
        header_rect = header.get_rect()
        header_rect.center = (self.player_2.rect.center[0] / 2, self.player_2.rect.center[1] / 2)
        
        self.player_2.surface.fill(WHITE)
        self.player_2.surface.blit(header, header_rect)
        self.surface.blit(self.player_2.surface, self.player_2.rect)

    def loop(self):
        global QUIT

        # Header message
        header = h1_b.render('Gomoku', True, WHITE, BLACK)
        header_rect = header.get_rect()
        header_rect.center = (self.width / 2, self.height / 2 - 400)

        #  message
        middle = h3_t.render('setup Game', True, WHITE, BLACK)
        middle_rect = middle.get_rect()
        middle_rect.center = (self.width / 2, self.height / 2 - 300)

        self.surface.fill(BLACK)
        self.surface.blit(header, header_rect)
        self.surface.blit(middle, middle_rect)

        while self.repeat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    self.repeat = False
                    continue
            self.draw_box_1()
            self.draw_box_2()
            self.window.blit(self)
            pygame.display.update()


class Final(Surface):
    """ 
    This class represents the surface of the end 
    state of the game.
    """
    def __init__(self, window):
        super().__init__(WIDTH, HEIGHT)
        self.repeat = True
        self._window = window
        self._winner = 2
        self._button = Button(self.width / 2, self.height / 2 + 200, "#000000", "#ffffff", "REMATCH", h3_t)

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
        header = h2_b.render('Game Finished!', True, WHITE, BLACK)
        header_rect = header.get_rect()
        header_rect.center = (self.width / 2, self.height / 2 - 100)
        
        # Mid-screen message
        if self.winner == 0:
            middle = h3_r.render('The game is a Tie', True, WHITE, BLACK)
        else:
            middle = h3_r.render(f'Player {self.winner} is Victorious', True, WHITE, BLACK)
        middle_rect = middle.get_rect()
        middle_rect.center = (self.width / 2, self.height / 2)

        # Put text on the surface
        self.surface.fill(BLACK)
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
        self._current_surface = 3


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

