from enum import Enum

class ColorEnum(Enum):
        Yellow = "Y"
        Red = "R"

class ConnectFourBoard:
    
   
    def __init__(self, c: int = 7, r: int = 6, w: int = 4) -> None:  
        self.num_cols = c #number of columns set by user, max is 26 (A-Z) min is 4
        self.num_rows = r #number of rows set by user, min is 4
        self.win_req = w #win requirement set by user
        self.current = [["_"]*self.num_cols for _ in range(self.num_rows)]
        self.columns = [[] for _ in range(c)]

    #function for printing out the current board and pieces played
    def print_board(self) -> None:

        for row_count, row in enumerate(self.current):
            print(str(row_count) + "  " + "  ".join(row))           

        column_title = [chr(x + ord("A")) for x in range(self.num_cols)] #create a list of column headers starting at "A"
        print("   " + "  ".join(column_title))


    #function for checking the validity of a chosen column. Checks if col exists and is not full. 
    def check_col(self, col: str) -> int:   
        col_i = ord(col) #using UNICODE of capital letters    
        unicode_A = ord("A")  # ord("A") == 65 
        if col_i < unicode_A or col_i > unicode_A -1 + self.num_cols: #max board size is 26 (A-Z)
            return -1 #error code -1 = column doesn't exist. TODO replace with Enum codes
        elif len(self.columns[col_i - unicode_A]) >= self.num_rows:
            return -2 #error code -2 = column is full
        else:
            return col_i - unicode_A

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

        while col - 1 - left_count >= 0 and self.current[row][col - 1 - left_count] == color: #while there is a column to the left and that piece is of same color
            left_count += 1

        while col + 1 + right_count < self.num_cols and self.current[row][col + 1 + right_count] == color: #while there is a column to the right and that piece is of same color
            right_count += 1 

        return 1 + left_count + right_count >= self.win_req   #current new piece + # of same color on left + # of same color on right

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

    def check_win(self, row: int, col: int, color: str) -> bool:
        return  self.__vertical_win(row, col, color) or self.__horizontal_win(row, col, color) or self.__diagonal_neg_slope(row, col, color) or self.__diagonal_pos_slope(row, col, color)



# Main gameplay. Set as while loop to play until exited.
class GameLoop:
    #TODO split up into smaller funcitons 
    
    def __init__(self) -> None:
        self.winner = None
        self.board = ConnectFourBoard()  #TODO add capability to change board size and win requirement

    def __game_won(self, player: str):
        self.board.print_board()
        print(player, "you win!! Press R to restart, or X to exit the game.")
        response = str(input()).capitalize() 
        if response == "R":
            self.board = ConnectFourBoard() #TODO what is best way to reinitialize the game? 
        else:
            self.winner = player

    def new_turn(self, player: str, color: str) -> None:
        self.board.print_board()

        print(player, "it is your turn. Enter the column you would like to add a piece to (A-G):")
        col_chosen = str(input()).capitalize() #TODO turn this query into a function, allow different input types
        
        col_code = self.board.check_col(col_chosen)  #TODO turn this into separate GameLoop method
        while col_code < 0:
            if col_code == -1:
                print(player + ", that column does not exist. Please pick another column ():") #TODO change to show flexible board size
                col_chosen = str(input()).capitalize()
                col_code = self.board.check_col(col_chosen)
            else:
                print(player + ", that column is full. Please pick another column ():") # TODO change to show flexible board size
                col_chosen = str(input()).capitalize()
                col_code = self.board.check_col(col_chosen)
        col_i = col_code

        self.board.columns[col_i].append(color)
        new_row, new_col = self.board.num_rows - len(self.board.columns[col_i]), col_i 

        #add new piece to board
        self.board.current[new_row][new_col] = color
        
        #check if new piece resulted in win
        if self.board.check_win(new_row, new_col, color):
            self.__game_won(player)


    

new_game = GameLoop()

# take player's names
print("Player 1, you are yellow. What is your name?")
player1 = str(input())
print("Player 2, you are red. What is your name?")
player2 = str(input())

while not new_game.winner:
    #first player's turn
    new_game.new_turn(player1, "Y")
    
    #second player's turn
    new_game.new_turn(player2, "R")


def tests() -> bool:
    return None
    #TODO add tests ..............................
    #check if board is printed correctly
    #check if pieces are added correctly
    #check if "column is full" check works
    #check if "column doesn't exist" works
    #check if win is correctly detected vertically, horizontally, diagonally
    #check if you can exit game at any time
    #check if you can restart game
