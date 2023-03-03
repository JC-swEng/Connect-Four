from enum import Enum

class PlayerColor(Enum):
    YELLOW = "Y"
    RED = "R"

class ErrorCode(Enum):
    VALID = 0
    COL_INVALID = 1
    COL_FULL = 2

class RunMode(Enum):
    TEST_MODE = 0
    PLAY_MODE = 1
    

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
    def check_col(self, col: str) -> ErrorCode:   
        #TODO add error handling of non-alpha inputs
        col_unicode = ord(col) #using UNICODE of capital letters    
        unicode_A = ord("A")  # ord("A") == 65 
        if col_unicode < unicode_A or col_unicode > unicode_A -1 + self.num_cols: #max board size is 26 (A-Z)
            return ErrorCode.COL_INVALID #error code 1 = column doesn't exist. 
        elif len(self.columns[col_unicode - unicode_A]) >= self.num_rows:
            return ErrorCode.COL_FULL #error code 2 = column is full
        else:
            return ErrorCode.VALID

    def is_board_full(self) -> bool:
        return sum(len(col) for col in self.columns) >= self.num_cols * self.num_rows

    def insert_new_piece(self, col: int, color) -> None:
        row = self.num_rows - 1 - len(self.columns[col])
        self.columns[col].append(color)
        self.current[row][col] = color
        return None

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
        return 1 + up_left + down_right >= self.win_req

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
        return 1 + up_right + down_left >= self.win_req

    def check_win(self, col: int, color: str) -> bool:
        row = self.num_rows - len(self.columns[col])
        return  self.__vertical_win(row, col, color) or self.__horizontal_win(row, col, color) or self.__diagonal_neg_slope(row, col, color) or self.__diagonal_pos_slope(row, col, color)

class InputOutput:
    def __init__(self, run_mode: RunMode, moves_list: list or None) -> None:
        self.run_mode = run_mode #if TRUE, user input will be asked for. Otherwise, input will be automatic from test functions
        self.moves_list = moves_list
        self.move_counter = 0

    def player_names(self) -> str:
        if self.run_mode is RunMode.PLAY_MODE:
            # take player's names
            print("Player 1, you are yellow. What is your name?")
            player1 = str(input())
            print("Player 2, you are red. What is your name?")
            player2 = str(input())
        else:
            player1, player2 = "player1", "player2"

        return player1, player2

    def game_over_IO(self, winner: str, board) -> str:
        print(str(board))
        if self.run_mode is RunMode.PLAY_MODE:
            if winner:
                print(f"{winner}, you win!! Press R to restart, or press any key to exit the game.")
                response = str(input())[0].capitalize() 
            else: # __game_over has been called without a winner
                print(f"The game has ended in a draw. Press R to restart, or press any key to exit the game.")
                response = str(input())[0].capitalize()
        else:
            response = "Exit"
        
        return response
    
    def select_col_IO(self, board, player: str) -> int:
        if self.run_mode is RunMode.PLAY_MODE:
            last_col = chr(ord('A') - 1 + board.num_cols)

            print(f"{player}, it is your turn. Enter the column you would like to add a piece to (A-{last_col}):")
            col = str(input())[0].capitalize()

            col_code = board.check_col(col)
            while col_code is not ErrorCode.VALID:
                if col_code is ErrorCode.COL_INVALID:
                    print(f"{player}, that column does not exist. Please pick another column (A-{last_col}):") 
                    col = str(input())[0].capitalize()
                    col_code = board.check_col(col)
                else:
                    print(f"{player}, that column is full. Please pick another column (A-{last_col}):") 
                    col = str(input())[0].capitalize()
                    col_code = board.check_col(col)
        
        else:
            col_code = None
            while col_code is not ErrorCode.VALID:
                col = self.moves_list[self.move_counter].capitalize()
                self.move_counter += 1 
                col_code = board.check_col(col)

        return ord(col) - ord('A')

    

# Main gameplay. Set as while loop to play until exited.
class GameLoop: 
    
    def __init__(self, run_mode: RunMode = RunMode.PLAY_MODE, moves_list: list = None) -> None:
        #self.run_mode = play_mode
        self.play = True
        self.winner = None
        self.player1 = None
        self.player2 = None
        #self.cols, self.rows, self.win_len = self.game_setup()
        self.input_output = InputOutput(run_mode, moves_list)
        self.board = ConnectFourBoard()  #TODO add capability to change board size and win requirement

    '''def game_setup() -> int:
        print(f"Welcome to Connect Four! Would you like to play with the standard board size and win requirement? Y/N")
        response = str(input())[0].capitalize()
        while True:
            if response == "Y":
                return 7, 6, 4
            elif response == "N":
                print(f"")
                response = str(input())[0].capitalize()
            else:
                print(f"Sorry, your input was not valid. Please type 'Y' for Yes or 'N' for No.")
                response = str(input())[0].capitalize()'''

    def __game_over(self) -> None:
        
        response = self.input_output.game_over_IO(self.winner, self.board)
        
        if response == "R":
            self.winner = None
            self.play = True
            self.board = ConnectFourBoard() 
        
        return None

    def new_turn(self, player: str, color: str) -> None:
        print(str(self.board))
        
        #validate column chosen and repeat user input request if column is invalid or full
        col_i = self.input_output.select_col_IO(self.board, player)
        
        #add new piece to board and to columns matrix
        self.board.insert_new_piece(col_i, color)
        
        #check if new piece resulted in win
        if self.board.check_win(col_i, color):
            self.winner = player
            self.play = False
        
        #check if board is full, possible draw scenario
        if self.board.is_board_full():
            self.play = False


    def play_game(self) -> str or None:
        self.player1, self.player2 = self.input_output.player_names()

        while self.play:
            #first player's turn
            self.new_turn(self.player1, PlayerColor.YELLOW.value)
            
            if self.play:
                #second player's turn
                self.new_turn(self.player2, PlayerColor.RED.value)
        
        self.__game_over()
        return self.winner


new_game = GameLoop(RunMode.PLAY_MODE)

'''while new_game.play:
    new_game.play_game()''' #UNCOMMENT TO PLAY THE GAME


def tests() -> None:
    #check if board is printed correctly
    #check if pieces are added correctly
    #check user input (char vs string for column)
    #check if "column is full" check works
    #check if "column doesn't exist" works
    #check if win is correctly detected vertically
    new_game = GameLoop(RunMode.TEST_MODE, ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B','A', 'B', 'A', 'B',])
    assert new_game.play_game() == "player1", "Player1 should have won, but did not."
    #check if win is correctly detected horizontally
    new_game = GameLoop(RunMode.TEST_MODE, ['A', 'A', 'B', 'B', 'c', 'c', 'd','d', 'B', 'A', 'B',])
    assert new_game.play_game() == "player1", "Player1 should have won, but did not."
    #check if win is correctly detected neg slope diagonally
    new_game = GameLoop(RunMode.TEST_MODE, ['d', 'c', 'c', 'b', 'a', 'b', 'b', 'a','e', 'a', 'A', 'e',])
    assert new_game.play_game() == "player1", "Player1 should have won, but did not."
    #check if win is correctly detected pos slope diagonally
    new_game = GameLoop(RunMode.TEST_MODE, ['A', 'B', 'B', 'C', 'D', 'C', 'C', 'd','e', 'd', 'd', 'B',])
    assert new_game.play_game() == "player1", "Player1 should have won, but did not."

    #check if you can exit game at any time
    #check if you can restart game
    print("All tests complete.")
    return None

tests()  #UNCOMMENT TO RUN TESTS
