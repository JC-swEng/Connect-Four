from enum import Enum

class ColorEnum(Enum):
    YELLOW = "Y"
    RED = "R"

class ErrorCodes(Enum):
    VALID = 0
    COL_INVALID = 1
    COL_FULL = 2

class ConnectFourBoard:
    
    def __init__(self, c: int = 7, r: int = 6, w: int = 4) -> None:  
        self.num_cols = c #number of columns set by user, max is 26 (A-Z) min is 4
        self.num_rows = r #number of rows set by user, min is 4
        self.win_req = w #win requirement set by user
        self.current = [["_"]*self.num_cols for _ in range(self.num_rows)]
        self.columns = [[] for _ in range(c)]

    #string representation of the board 
    def __str__(self) -> str:
        board_str = "\n".join(f"{row_count}  {'  '.join(row)}" for row_count, row in enumerate(self.current))
        column_title = [chr(x + ord("A")) for x in range(self.num_cols)] #create a list of column headers starting at "A"
        board_str += f"\n   {'  '.join(column_title)}"

        return board_str

    #function for checking the validity of a chosen column. Checks if col exists and is not full. 
    def check_col(self, col: str) -> ErrorCodes:   
        col_unicode = ord(col) #using UNICODE of capital letters    
        unicode_A = ord("A")  # ord("A") == 65 
        if col_unicode < unicode_A or col_unicode > unicode_A -1 + self.num_cols: #max board size is 26 (A-Z)
            return ErrorCodes.COL_INVALID #error code 1 = column doesn't exist. TODO replace with Enum codes
        elif len(self.columns[col_unicode - unicode_A]) >= self.num_rows:
            return ErrorCodes.COL_FULL #error code 2 = column is full
        else:
            return ErrorCodes.VALID

    def insert_new_piece(self, col: int, color) -> int:
        row = (self.num_rows - 1 - len(self.columns[col]))
        self.columns[col].append(color)
        self.current[row][col] = color
        return 0

    def __vertical_win(self, row: int, col: int, color: str) -> bool:
        if row <= self.num_rows - self.win_req: #if the current row is high enough to have a winning quantity
            adjacent_count = 1
            while adjacent_count + row < self.num_rows: #do until reaching the bottom of board
                if self.current[adjacent_count + row][col] == color:
                    adjacent_count += 1
                    if adjacent_count >= self.win_req:
                        return True
                else:
                    return False
        return False

    def __horizontal_win(self, row: int, col: int, color: str) -> bool:

        left_count, right_count = 0, 0

        #while there is a column to the left and that piece is of same color
        while col - 1 - left_count >= 0 and self.current[row][col - 1 - left_count] == color: 
            left_count += 1

        #while there is a column to the right and that piece is of same color
        while col + 1 + right_count < self.num_cols and self.current[row][col + 1 + right_count] == color: 
            right_count += 1 

        #current new piece + # of same color on left + # of same color on right
        return 1 + left_count + right_count >= self.win_req   

    def __diagonal_neg_slope(self, row: int, col: int, color: str) -> bool:
        #check upper left diagonal + lower right diagonal (negative slope)
        up_left, down_right = 0, 0
        while col - 1 - up_left >= 0 and row - 1 - up_left >= 0:
            if self.current[row - 1 - up_left][col - 1 - up_left] == color:
                up_left += 1
            else:
                break
        while col + 1 + down_right < self.num_cols and row + 1 + down_right < self.num_rows:
            if self.current[row + 1 + down_right][col + 1 + down_right] == color:
                down_right += 1
            else:
                break
        return up_left + down_right >= self.win_req

    def __diagonal_pos_slope(self, row: int, col: int, color: str) -> bool:
        #check upper right diagonal + lower left diagonal (positive slope)
        up_right, down_left = 0, 0
        while col - 1 - down_left >= 0 and row + 1 + down_left < self.num_rows:
            if self.current[row + 1 + down_left][col - 1 - down_left] == color:
                down_left += 1
            else:
                break
        while col + 1 + up_right < self.num_cols and row - 1 - up_right >= 0:
            if self.current[row - 1 - up_right][col + 1 + up_right] == color:
                up_right += 1
            else:
                break
        return up_right + down_left >= self.win_req

    def check_win(self, col: int, color: str) -> bool:
        row = (self.num_rows - len(self.columns[col]))
        return  self.__vertical_win(row, col, color) or self.__horizontal_win(row, col, color) or self.__diagonal_neg_slope(row, col, color) or self.__diagonal_pos_slope(row, col, color)



# Main gameplay. Set as while loop to play until exited.
class GameLoop:
    #TODO split up into smaller funcitons 
    
    def __init__(self) -> None:
        self.winner = None
        self.board = ConnectFourBoard()  #TODO add capability to change board size and win requirement

    def __game_won(self, player: str) -> None:
        print(str(self.board))
        print(f"{player}, you win!! Press R to restart, or X to exit the game.")
        response = str(input()).capitalize() 
        if response == "R":
            self.board = ConnectFourBoard() #TODO what is best way to reinitialize the game? 
        else:
            self.winner = player

    def __select_col(self, player: str) -> int:
        last_col = chr(ord('A')-1+self.board.num_cols)

        print(f"{player}, it is your turn. Enter the column you would like to add a piece to (A-{last_col}):")
        col = str(input()).capitalize() #TODO turn this query into a function, allow different input types

        col_code = self.board.check_col(col)
        while col_code is not ErrorCodes.VALID:
            if col_code is ErrorCodes.COL_INVALID:
                print(f"{player}, that column does not exist. Please pick another column (A-{last_col}):") 
                col = str(input()).capitalize()
                col_code = self.board.check_col(col)
            else:
                print(f"{player}, that column is full. Please pick another column (A-{last_col}):") 
                col = str(input()).capitalize()
                col_code = self.board.check_col(col)
        
        return ord(col) - ord('A')

    def new_turn(self, player: str, color: str) -> None:
        print(str(self.board))
        
        #validate column chosen and repeat user input request if column is invalid or full
        col_i = self.__select_col(player)
        
        #add new piece to board and to columns matrix
        self.board.insert_new_piece(col_i, color)
        
        #check if new piece resulted in win
        if self.board.check_win(col_i, color):
            self.__game_won(player)


    

new_game = GameLoop()

#TODO move into new method of gameloop class
# take player's names
print("Player 1, you are yellow. What is your name?")
player1 = str(input())
print("Player 2, you are red. What is your name?")
player2 = str(input())

while not new_game.winner:
    #first player's turn
    new_game.new_turn(player1, ColorEnum.YELLOW.value)
    
    #second player's turn
    new_game.new_turn(player2, ColorEnum.RED.value)


def tests() -> bool:
    return None
    #TODO add tests ..............................
    #check if board is printed correctly
    #check if pieces are added correctly
    #check user input (char vs string for column)
    #check if "column is full" check works
    #check if "column doesn't exist" works
    #check if win is correctly detected vertically, horizontally, diagonally
    #check if you can exit game at any time
    #check if you can restart game
