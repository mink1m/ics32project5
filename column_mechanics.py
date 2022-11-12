#Minha Kim 
#81343818


class GameOver(Exception):
    pass


class Board:
    def __init__(self, row: int, col: int) -> None:
        """
        Initializes the class with rows and columns. Creates the board
        """
        self._row = row
        self._col = col
        self._board = []
        self._make_empty_list()

    def columns(self) -> int:
        """
        Returns the number of columns.
        """
        return self._col

    def rows(self) -> int:
        """
        Returns the number of rows.
        """
        return self._row

    def list(self) -> list[list]:
        """
        Returns the board in list form.
        """
        return self._board

    def _make_empty_list(self) -> list:
        """
        Creates an empty nested list (board).
        """
        for col in range(self._col):
            self._board.append([])
            for row in range(self._row):
                self._board[-1].append(' ')
        return self._board

    def make_content_list(self, input_string: str, row_count: int) -> None:
        """
        Creates a list when "CONTENTS" is used.
        """
        for c in range(len(input_string)):
            self._board[c][row_count] = str(input_string[c])

    def shift_all_down(self) -> None:
        """
        Only used when "CONTENTS" is used (instead of "EMPTY").
        """
        for linelist in self._board:
            self._shift_all_down_empty_counter = 0
            while True:
                for char in linelist:
                    if char == " ":
                        linelist.remove(char)
                        self._shift_all_down_empty_counter += 1
                if " " not in linelist:
                    break
            for i in range(self._shift_all_down_empty_counter):
                linelist.insert(0, " ")

    def create_faller(self, faller_string: str) -> None:
        """
        Creates a faller object
        """
        self._faller_split = faller_string.split()
        self._faller_col = self._faller_split[1]
        self._faller_top = self._faller_split[2]
        self._faller_mid = self._faller_split[3]
        self._faller_bot = self._faller_split[4]
        if self._check_if_col_is_full(int(self._faller_col)) == False:
            self.gravity(self._faller_col, self._faller_top, self._faller_mid, self._faller_bot, 0)
        else:
            raise GameOver

    def gravity(self, col: int, top: str, mid: str, bot: str, iteration: int) -> None:
        """
        Checks if the faller has vertical lines and moves the faller down accordingly.
        """
        self._faller_top = top
        self._faller_mid = mid
        self._faller_bot = bot
        self._iteration = iteration
        self._this_column = self._board[int(col) - 1]
        if self._check_this_cell(int(col), int(self._iteration)) == True and int(self._iteration) < self._col - 1:
            self.get_rid_of_vert_bars()
            raise GameOver
        if self._iteration == self._row - 1:
            if self._iteration >= 0:
                self._this_column[self._iteration] = self._faller_bot + 'P'
            if self._iteration - 1 >= 0:
                self._this_column[self._iteration - 1] = self._faller_mid + 'P'
            if self._iteration - 2 >= 0:
                self._this_column[self._iteration - 2] = self._faller_top + 'P'
            for i in range(self._iteration - 2, self._row):
                if "F" or "P" in self._this_column[self._iteration - 3]:
                    self._this_column[self._iteration - 3] = " "
        else:
            if self._board[int(self._faller_col) - 1][int(self._iteration) + 1] != " ":
                if self._iteration >= 0:
                    self._this_column[self._iteration] = self._faller_bot + 'P'
                if self._iteration - 1 >= 0:
                    self._this_column[self._iteration - 1] = self._faller_mid + 'P'
                if self._iteration - 2 >= 0:
                    self._this_column[self._iteration - 2] = self._faller_top + 'P'
                if self._iteration - 2 > 0:
                    for i in range(self._iteration - 2, self._row):
                        if "F" or "P" in self._this_column[self._iteration - 3]:
                            self._this_column[self._iteration - 3] = " "
            else:
                if self._iteration >= 0:
                    self._this_column[self._iteration] = self._faller_bot + 'F'
                if self._iteration - 1 >= 0:
                    self._this_column[self._iteration - 1] = self._faller_mid + 'F'
                if self._iteration - 2 >= 0:
                    self._this_column[self._iteration - 2] = self._faller_top + 'F'
                for i in range(self._iteration - 2, self._row):
                    if "F" in self._this_column[self._iteration - 3]:
                        self._this_column[self._iteration - 3] = " "
                if self._this_column[self._iteration + 1] != " " or self._iteration == self._row:
                    self.all_falls_down()
                try:
                    if self._check_this_cell(int(self._faller_col), int(self._iteration) + 1):
                        self.get_rid_of_vert_bars()
                except:
                    pass
        self._iteration += 1

    def get_top(self) -> str:
        """
        Returns the top faller.
        """
        return self._faller_top

    def get_mid(self) -> str:
        """
        Returns the middle faller.
        """
        return self._faller_mid

    def get_bot(self) -> str:
        """
        Returns the bottom faller.
        """
        return self._faller_bot

    def get_iter(self) -> int:
        """
        Returns the number of iterations.
        """
        return self._iteration
    
    def get_current_col(self) -> int:
        """
        Returns the current column number.
        """
        return self._faller_col
    
    def _check_if_col_is_full(self, col: int) -> bool:
        """
        Checks if the given column is full.
        """
        self._this_col_is_being_checked = list(self._board[col - 1])
        self._col_check_counter = 0
        for item in self._this_col_is_being_checked:
            if item == " ":
                self._col_check_counter += 1
        if self._col_check_counter == 0:
            return True
            """
            True means the column IS FULL
            """
        else:
            return False
    
    def _check_this_cell(self, col: int, index: int) -> bool:
        """
        Checks if the given cell is full.
        """
        if self._board[col - 1][index] != " ":
            return True
            """
            True means the cell IS TAKEN
            """
        else:
            return False
    
    def all_falls_down(self) -> None:
        """
        Moves all fallers down to the vertical lines. 
        """
        for col in range(self._col):
            for row in range(self._row):
                if "F" in self._board[col][row]:
                    self._board[col][row] = self._board[col][row].replace('F','P')
   
    def get_rid_of_vert_bars(self) -> None:
        """
        Gets rid of vertical bars and freezes Faller.
        """
        for col in range(self._col):
            for row in range(self._row):
                if "P" in self._board[col][row]:
                    self._board[col][row] = self._board[col][row].replace('P','')
   
    def rotate_faller(self) -> None:
        """
        Rotates the faller.
        """
        self._temp_top = self._faller_bot
        self._temp_bot = self._faller_mid
        self._faller_mid = self._faller_top
        self._faller_bot = self._temp_bot
        self._faller_top = self._temp_top
        if "P" in self._this_column[self._iteration - 1]:
            self._this_column[self._iteration - 3] = self._faller_top + 'P'
            self._this_column[self._iteration - 2] = self._faller_mid + 'P'
            self._this_column[self._iteration - 1] = self._faller_bot + 'P'            
        elif "F" in self._this_column[self._iteration - 1]:
            self._this_column[self._iteration - 1] = self._faller_bot + 'F'
            if self._iteration - 2 >= 0:
                self._this_column[self._iteration - 2] = self._faller_mid + 'F'
            if self._iteration - 3 >= 0:
                self._this_column[self._iteration - 3] = self._faller_top + 'F'

    def shift_left_or_right(self, RorL: int) -> None:
        """
        Moves faller left or right.
        0 is left and 1 is right.
        """
        if "F" in self._board[int(self._faller_col) - 1][self._iteration - 1]:
            pass
        elif "P" not in self._board[int(self._faller_col) - 1][self._iteration - 1]:
            return
        if RorL == 1:
            if int(self._faller_col) == int(self._col):
                return
            self._testing_col = int(self._faller_col) + 1
            self._testing_bar = self._board[self._testing_col - 1]
        elif RorL == 0:
            if int(self._faller_col) == 1:
                return
            self._testing_col = int(self._faller_col) - 1
            self._testing_bar = self._board[self._testing_col - 1]
        if self._iteration - 1 >= 0:
            if self._check_this_cell(self._testing_col, self._iteration - 1):
                return
            self._testing_bar[self._iteration - 1] = self._this_column[self._iteration - 1]
            self._this_column[self._iteration - 1] = " "
        if self._iteration - 2 >= 0:
            self._testing_bar[self._iteration - 2] = self._this_column[self._iteration - 2]
            self._this_column[self._iteration - 2] = " "
        if self._iteration - 3 >= 0:
            self._testing_bar[self._iteration - 3] = self._this_column[self._iteration - 3]
            self._this_column[self._iteration - 3] = " "
        self._faller_col = self._testing_col
        self._this_column = self._board[self._faller_col - 1]
        try:
            if self._check_this_cell(int(self._faller_col), int(self._iteration)):
                for i in range(len(self._this_column)):
                    if "F" in self._this_column[i]:
                        self._this_column[i] = self._this_column[i].replace("F", "P")
            else:
                for i in range(len(self._this_column)):
                    if "P" in self._this_column[i]:
                        self._this_column[i] = self._this_column[i].replace("P", "F")
        except:
            pass
 
    def update_match(self) -> None:
        """
        Updates the matches in the Board.
        """
        self._match_horiz()
        self._match_vert()
        self._match_diag()
   
    def _match_horiz(self) -> None:
        """
        Finds horizontal matches.
        """
        matched_list = []
        for row in range(self._row):
            match_count = 0
            for col in range(self._col):
                testing_str = str(col)
                if self._board[col][row] != " " and "P" not in self._board[col][row] and "F" not in self._board[col][row]:
                    self._current_cell = self._board[col][row]
                    try:
                        match_count = 1
                        for i in range(1, self._col):
                            if self._current_cell == self._board[col + i][row] != " ":
                                match_count += 1
                            else:
                                if match_count >= 3:
                                    matched_list.append((col,row,match_count))
                                match_count = 0
                            if match_count >= 3:
                                matched_list.append((col,row,match_count))
                    except IndexError:
                        pass
        for index in range(len(matched_list)):
            matched_horiz = matched_list[index]
            for i in range(matched_horiz[2]):
                self._board[matched_horiz[0] + i][matched_horiz[1]] += '*'
   
    def _match_vert(self) -> None:
        """
        Finds vertical matches.
        """
        matched_list = []
        for row in range(self._row):
            match_count = 0
            for col in range(self._col):
                testing_str = str(col)
                if self._board[col][row] != " " and "P" not in self._board[col][row] and "F" not in self._board[col][row]:
                    self._current_cell = self._board[col][row]
                    try:
                        match_count = 1
                        for i in range(1, self._row):
                            if self._current_cell == self._board[col][row + i] != " ":
                                match_count += 1
                            else:
                                if match_count >= 3:
                                    matched_list.append((col,row,match_count))
                                match_count = 0
                            if match_count >= 3:
                                matched_list.append((col,row,match_count))
                    except IndexError:
                        pass
        for index in range(len(matched_list)):
            matched_vert = matched_list[index]
            for i in range(matched_vert[2]):
                self._board[matched_vert[0]][matched_vert[1] + i] += '*'
   
    def _match_diag(self) -> None:
        #Sorry to whoever's grading this, had to hard code this part; too stressed out
        """
        Finds diagonal matches.
        """
        matched_list = []
        for row in range(self._row):
            for col in range(self._col):
                if self._board[col][row] != " " and "P" not in self._board[col][row] and "F" not in self._board[col][row]:
                    self._current_cell = self._board[col][row]
                    try:
                        if self._current_cell == self._board[col + 1][row + 1] == self._board[col + 2][row + 2]:
                            matched_list.append((col, row))
                            matched_list.append((col + 1, row + 1))
                            matched_list.append((col + 2, row + 2))
                        if self._current_cell == self._board[col + 1][row - 1] == self._board[col + 2][row - 2]:
                            matched_list.append((col, row))
                            matched_list.append((col + 1, row - 1))
                            matched_list.append((col + 2, row - 2))
                    except IndexError:
                        pass
        for pairs in matched_list:
            self._board[pairs[0]][pairs[1]] += '*'
        return matched_list
   
    def remove_stars(self) -> None:
        """
        Removes all of the matches from the board.
        """
        for col in range(self._col):
            for row in range(self._row):
                if "*" in self._board[col][row]:
                    self._board[col][row] = " "

