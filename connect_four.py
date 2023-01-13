
class Board():
    self.current = [[None]*7 for _ in range(6)]
    self.colA, self.colB, self.colC, self.colD, self.colE, self.colF, self.colG = [], [], [], [], [], [], []
    self.columns = [colA, colB, colC, colD, colE, colF, colG]
    self.col_dict = {"A": [colA, 0], "B": [colB, 1], "C": [colC, 2], "D": [colD, 3], "E": [colE, 4], "F": [colF, 5], "G": [colG, 6]}

    def __init__(self):

    #function for printing out the current board and pieces played
    def print_board(board):
        row_count = 6
        for row in board:
            print_row = str(row_count)
            
            for elem in row:
                if elem is None:
                    print_row += " _ "
                else:
                    print_row += " " + elem + " "

            print(print_row)
            row_count -= 1
        
        print("  A  B  C  D  E  F  G")


    #function for checking the validity of a chosen column. Checks if col exists and is not full. 
    def check_col(col: str): 
        while True:        
            if col not in self.col_dict: 
                print(player1 + ", that column does not exist. Please pick another column (A-G):")
                col = str(input()).capitalize()
                continue
            
            elif len(self.col_dict[col][0]) >= 6:
                print(player1 + ", that column is full. Please pick another column (A-G):")
                col = str(input()).capitalize()
                continue
            else:
                return self.col_dict[col]

    def vertical_win([row, col], color: str):
        #vertical win
        if row <= 2:
            adj_count = 1
            while adj_count + row <= 5: 
                if board[row + adj_count][col] == color:
                    adj_count += 1
                    if adj_count >= 4:
                        return True
                else:
                    adj_count = 0
        
        return False

    def horizontal_win([row, col], color):
        #horizontal win
        adj_count = 0
        for x in range(7): 
            if board[row][x] == color:
                adj_count += 1
                if adj_count >= 4:
                    return True
            else:
                    adj_count = 0
        
        return False

    def diagonal_win([row, col], color):
        #diagonal win
        
        #TODO.........................................

    def check_win([row, col], color):
        win = False
        win = vertical_win([row, col], color) or horizontal_win([row, col], color) or diagonal_win([row, col], color)
        return win



# Main gameplay. Set as while loop to play until exited.
class GameLoop():
    winner = None

    def new_turn(player: str, color: str):
        print(player, "it is your turn. Enter the column you would like to add a piece to (A-G):")
        col_chosen = str(input()).capitalize()
        valid_col, col_i = check_col(col_chosen)
        valid_col.append(color)
        new_piece = [6 - len(valid_col), col_i]

        #add new piece to board and print current board
        board[new_piece[0]][new_piece[1]] = color
        print_board(board)

        #check if new piece resulted in win
        if check_win(new_piece, color):
            winner = player
            print(player, "you win!! Press R to restart, or X to exit the game.")
            #TODO.........................................


    # take player's names
    print("Player 1, you are yellow. What is your name?")
    player1 = str(input())
    print("Player 2, you are red. What is your name?")
    player2 = str(input())

    while not winner:
        #first player's turn
        new_turn(player1, "Y")
        
        #second player's turn
        new_turn(player2, "R")


def tests():
    #TODO add tests ..............................
    #check if board is printed correctly
    #check if pieces are added correctly
    #check if "column is full" check works
    #check if "column doesn't exist" works
    #check if win is correctly detected vertically, horizontally, diagonally
    #check if you can exit game at any time
    #check if you can restart game
