
colA, colB, colC, colD, colE, colF, colG = [], [], [], [], [], [], []

board = [[None]*7 for _ in range(6)]

winner = None

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

printBoard(board)

while not winner:
    print("Player 1, you are yellow. What is your name?")
    player1 = str(input())
    print("Player 2, you are red. What is your name?")
    player2 = str(input())