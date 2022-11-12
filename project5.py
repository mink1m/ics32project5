#81343818
#Minha Kim

import pygame
import column_mechanics
import random
from column_mechanics import GameOver


#Color constants
_white = (255,255,255)
_red = (255,0,0)
_orange = (255, 127, 0)
_yellow = (255, 255, 0)
_green = (0, 255, 0)
_blue = (0,0,255)
_purple = (75, 0, 130)
_pink = (255,53,185)
_black = (0,0,0)


def check_for_verts(game_list: list) -> bool:
    """
    Checks for vertical lines (|x|) in the Board. True if found.
    """
    for item in game_list:
        if "P" in str(item):
            return True
    else:
        return False


def check_for_fallers(game_list: list) -> bool:
    """
    Checks for fallers ([x]) in the board. True if found.
    """
    for item in game_list:
        if "F" in str(item):
            return True
    else:
        return False


class ColumnsGame:
    def __init__(self) -> None:
        """
        Initializes the game by creating the row, column, and gem values. Also creates
        the game board.
        """
        self._running = True
        self._row = 13
        self._col = 6
        self._gem_list = ["S", "T", "V", "W", "X", "Y", "Z"]
        self._board = column_mechanics.Board(self._row, self._col)

    def run(self) -> None:
        """
        Runs the game.
        """
        pygame.init()
        self._change_surface((300, 600))
        clock = pygame.time.Clock()
        try:
            while self._running:
                clock.tick(1)
                self._is_faller_present = self._check_board_for_no_fallers(self._board.list())
                if self._is_faller_present:
                    self._create_faller()
                else:
                    self._handle_events()
                self._redraw()
            pygame.quit()
        except:
            pygame.quit()

    def _check_board_for_no_fallers(self, board: column_mechanics.Board) -> None:
        """
        Checks if there are fallers in the board
        """
        for c in board:
            for r in c:
                if "F" in r or "P" in r or "*" in r:
                    return False
        return True

    def _create_faller(self) -> None:
        """
        Creates the faller
        """
        self._faller_str = f"F {self._generate_random_column()} {self._generate_random_faller()} {self._generate_random_faller()} {self._generate_random_faller()}"
        self._board.create_faller(self._faller_str)

    def _generate_random_faller(self) -> str:
        """
        Generates a random faller (three random letters)
        """
        return str(random.choice(self._gem_list))
    
    def _generate_random_column(self) -> int:
        """
        Generates a random column number
        """
        return str(random.randint(1,6))

    def _change_surface(self, dimensions: tuple) -> None:
        """
        Creates and updates the surface
        """
        pygame.display.set_mode(dimensions, pygame.RESIZABLE)
        self._surface = pygame.display.get_surface()
        self._width, self._height = self._surface.get_size()
    
    def _handle_events(self) -> None:
        """
        Handles all events (resizing, exiting, space, left, right)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.VIDEORESIZE:
                self._change_surface(event.size)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._board.rotate_faller()
                if event.key == pygame.K_LEFT:
                    self._board.shift_left_or_right(0)
                if event.key == pygame.K_RIGHT:
                    self._board.shift_left_or_right(1)
        self._faller_gravity()

    def _faller_gravity(self) -> None:
        """
        Moves the faller down.
        """
        try:
            self._board.gravity(self._board.get_current_col(), self._board.get_top(), 
            self._board.get_mid(), self._board.get_bot(), self._board.get_iter())
        except GameOver:
            raise GameOver
        except IndexError:
            vert_bool = check_for_verts(self._board.list()[int(self._board.get_current_col()) - 1])
            if vert_bool:
                self._board.get_rid_of_vert_bars()
                self._board.update_match()
            else:
                self._board.all_falls_down()

    def _grid(self) -> None:
        """
        Creates the grid on the display
        """
        for c in range(1,7):
            pygame.draw.line(self._surface, _white, (int(self._width*(c/6)), 0), (int(self._width*(c/6)), self._height), 1)
        for r in range(1,14):
            pygame.draw.line(self._surface, _white, (0, int(self._height*(r/13))), (self._width, int(self._height*(r/13))), 1)
   
    def _gems(self) -> None:
        """
        Creates the gems on the display and shows the effect when the gems land.
        """
        for c in range(self._col):
            for r in range(self._row):
                xval = (.5 + c) / 6 * self._width
                yval = (.5 + r) / 13 * self._height
                pygame.draw.circle(self._surface, self._color_from_letter(self._board.list()[c][r]), 
                (xval,yval), self._height / 40)
                if "P" in self._board.list()[c][r]:
                    pygame.draw.circle(self._surface, _white, (xval,yval), self._height / 45)

    def _color_from_letter(self, char: str) -> tuple:
        """
        Returns colors from the letter given.
        """
        if "S" in char:
            return _red
        elif "T" in char:
            return _orange
        elif "V" in char:
            return _yellow
        elif "W" in char:
            return _green
        elif "X" in char:
            return _blue
        elif "Y" in char:
            return _purple
        elif "Z" in char:
            return _pink
        elif char == " ":
            return _black
        
    def _redraw(self) -> None:
        """
        Redraws the surface with the grid and gems.
        """
        self._gems()
        self._grid()
        pygame.display.flip()

if __name__ == "__main__":
    ColumnsGame().run()

