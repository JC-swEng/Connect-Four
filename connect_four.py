
class Board:
   
    def __init__(self, c: int = 7, r: int = 6, w: int = 4) -> None:  
        self.num_cols = c #number of columns set by user
        self.num_rows = r #number of rows set by user
        self.win_req = w #win requirement set by user
        self.current = [[None]*self.num_cols for _ in range(self.num_rows)]
        self.colA, self.colB, self.colC, self.colD, self.colE, self.colF, self.colG = [], [], [], [], [], [], [] #TODO need to change to 2D matrix
        self.columns = [self.colA, self.colB, self.colC, self.colD, self.colE, self.colF, self.colG]
        self.col_dict = {"A": [self.colA, 0], "B": [self.colB, 1], "C": [self.colC, 2], "D": [self.colD, 3], "E": [self.colE, 4], "F": [self.colF, 5], "G": [self.colG, 6]}  
                #TODO need to fix col_dict to flex to input board size

    #function for printing out the current board and pieces played
    def print_board(self) -> None:
        row_count = self.num_rows
        for row in self.current:
            print_row = str(row_count)
            
            for elem in row:
                if elem is None:
                    print_row += " _ "
                else:
                    print_row += " " + elem + " "

            print(print_row)
            row_count -= 1
        
        print("  A  B  C  D  E  F  G")  #TODO needs to flex to board size


    #function for checking the validity of a chosen column. Checks if col exists and is not full. 
    def check_col(self, col: str): 
        while True:        
            if col not in self.col_dict: 
                print(player1 + ", that column does not exist. Please pick another column (A-G):")
                col = str(input()).capitalize()
                continue
            
            elif len(self.col_dict[col][0]) >= self.num_rows:
                print(player1 + ", that column is full. Please pick another column (A-G):")
                col = str(input()).capitalize()
                continue
            else:
                return self.col_dict[col]

    def __vertical_win(self, row: int, col: int, color: str) -> bool:
        if row <= self.num_rows - self.win_req: 
            adj_count = 1
            while adj_count + row <= 5: #TODO must change to make flex to board size
                if self.current[row + adj_count][col] == color:
                    adj_count += 1
                    if adj_count >= self.win_req:
                        return True
                else:
                    adj_count = 0
        
        return False

    def __horizontal_win(self, row: int, col: int, color: str) -> bool:
        #TODO change logic to be # of same color on left + # of same color on right
        adj_count = 0
        for col in range(self.num_cols): 
            if self.current[row][col] == color:
                adj_count += 1
                if adj_count >= self.win_req:
                    return True
            else:
                    adj_count = 0
        
        return False

    def __diagonal_win(self, row: int, col: int, color: str) -> bool:
        return False
        #TODO.........................................

    def check_win(self, row: int, col: int, color: str) -> bool:
        win = __vertical_win(row, col, color) or __horizontal_win(row, col, color) or __diagonal_win(row, col, color)
        return win



# Main gameplay. Set as while loop to play until exited.
class GameLoop:
    #TODO split up into smaller funcitons 
    
    def __init__(self) -> None:
        self.winner = None
        self.board = Board()  #TODO add capability to change board size and win requirement

    def __game_won():
        print(player, "you win!! Press R to restart, or X to exit the game.")
        response = str(input()).capitalize() 
        if response == "R":
            self.board = Board() #TODO what is best way to reinitialize the game? 
        else:
            self.winner = player

    def new_turn(player: str, color: str) -> None:
        print(player, "it is your turn. Enter the column you would like to add a piece to (A-G):")
        col_chosen = str(input()).capitalize() #TODO turn this query into a function, allow different input types
        valid_col, col_i = self.board.check_col(col_chosen)
        valid_col.append(color)
        new_row, new_col = self.board.num_rows - len(valid_col), col_i 

        #add new piece to board and print current board
        self.board.current[new_row][new_col] = color
        self.board.print_board()

        #check if new piece resulted in win
        if self.board.check_win(new_row, new_col, color):
            self.__game_won()


    

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
    #TODO add tests ..............................
    #check if board is printed correctly
    #check if pieces are added correctly
    #check if "column is full" check works
    #check if "column doesn't exist" works
    #check if win is correctly detected vertically, horizontally, diagonally
    #check if you can exit game at any time
    #check if you can restart game
