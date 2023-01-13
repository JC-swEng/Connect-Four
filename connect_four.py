
colA, colB, colC, colD, colE, colF, colG = [], [], [], [], [], [], []
columns = [colA, colB, colC, colD, colE, colF, colG]

board = [[None]*7 for _ in range(6)]

winner = None

#function for printing out the current board and pieces played
def printBoard(board):
    col_count = 6
    for row in board:
        print_row = str(col_count)
        
        for elem in row:
            if elem is None:
                print_row += " _ "
            else:
                print_row += " " + elem + " "

        print(print_row)
        col_count -= 1
    
    print("  A  B  C  D  E  F  G")


#function for checking the validity of a chosen column. Checks if col exists and is not full. 
def checkCol(col):
    while True:
        match col:
            case "A":
                col = colA
                col_index = 0
            case "B":
                col = colB
                col_index = 1
            case "C":
                col = colC
                col_index = 2
            case "D":
                col = colD
                col_index = 3
            case "E":
                col = colE
                col_index = 4
            case "F":
                col = colF
                col_index = 5
            case "G":
                col = colG
                col_index = 6
            case _:
                col = None
        
        if not col: 
            print(player1 + ", that column does not exist. Please pick another column (A-G):")
            col = str(input()).capitalize()
            continue
        
        elif len(col) >= 6:
            print(player1 + ", that column is full. Please pick another column (A-G):")
            col = str(input()).capitalize()
            continue
        else:
            return col, col_index


def checkWin([row, col], color):
    win = False
    #vertical win
    if row <= 2:
        adj_count = 1
        while adj_count + row <= 5: 
            if board[row + adj_count][col] == color:
                adj_count += 1
                if adj_count >= 4:
                    win = True
                    return win
            else:
                adj_count = 0

    #horizontal win
    adj_count = 0
    for x in range(7): 
        if board[row][x] == color:
            adj_count += 1
            if adj_count >= 4:
                win = True
                return win
        else:
            adj_count = 0

    #diagonal win
    
    #TODO.........................................

    return win


printBoard(board)
# take player's names
print("Player 1, you are yellow. What is your name?")
player1 = str(input())
print("Player 2, you are red. What is your name?")
player2 = str(input())

# Main gameplay. Set as while loop to play until exited.
while not winner:
    
    #first player's turn
    print(player1, "it is your turn. Enter the column you would like to add a piece to (A-G):")
    col_chosen = str(input()).capitalize()
    valid_col, col_i = checkCol(col_chosen)
    valid_col.append("Y")
    new_piece = [6 - len(valid_col), col_i]

    #add new piece to board and print current board
    board[new_piece[0]][new_piece[1]] = "Y"
    printBoard(board)

    #check if new piece resulted in win
    if checkWin(new_piece, "Y"):
        winner = player1
        print(player1, "you win!! Press R to restart, or X to exit the game.")
        #TODO.........................................

    
    #second player's turn
    print(player2, "it is your turn. Enter the column you would like to add a piece to (A-G):")
    col_chosen = str(input()).capitalize()
    valid_col, col_i = checkCol(col_chosen)
    valid_col.append("R")
    new_piece = [6 - len(valid_col), col_i]

    #add new piece to board and print current board
    board[new_piece[0]][new_piece[1]] = "R"
    printBoard(board)

    #check if new piece resulted in win
    if checkWin(new_piece, "R"):
        winner = player2
        print(player2, "you win!! Press R to restart, or X to exit the game.")
        #TODO.........................................

