""" 
A library of different methods to solve a sodoku board.
https://en.wikipedia.org/wiki/Sudoku_solving_algorithms 
^ Where I will be pulling different algorithm types from
"""

# Recursively checks all the possible values that could solve the board until it encounters a solution. This is a brute force approach.
def backtracking(board):

    # Variable to keep track of whether or not the board has been solved
    global solved
    solved = False
    
    # given a value and a postion, returns a boolean of if value can go there
    def __check_if_possible(value, position):
        # check row
        for i in range(9):
            if board[position[0]][i] == str(value):
                return False

        # check column
        for i in range(9):
            if board[i][position[1]] == str(value):
                return False

        # check box
        for i in range(int(position[0] / 3) * 3, int(position[0] / 3) * 3 + 3):
            for k in range(int(position[1] / 3) * 3, int(position[1] / 3) * 3+ 3):
                if board[i][k] == str(value):
                    return False
        
        return True
    
    # fnction to solve the given board
    def __back_helper(board):
        global solved

        # Check every position and see if it is blank or a zero
        for x in range(9):
            for y in range(9):
                if board[x][y] == '' or board[x][y] == '0':

                    # When we find a blank, test all possible values
                    for val in range(1, 10):

                        # Checks if the current value is possible in the current location
                        if __check_if_possible(val, (x, y)):
                            # Store the possible value in the position in board
                            board[x][y] = str(val)
                            # Find the next possible value
                            __back_helper(board)
                            # If we get here, we know the board is either solved, or our guess for the location was wrong
                            # If it's wrong, we simply set the value back to ''
                            if not solved:
                                board[x][y] = ''
                    # How we know that a guess was wrong. If we get here, we didn't find a possible value for the current position
                    return

        # If we have succesfully made it through the loop, that means we did not find any blanks or zeros so we know it must be solved
        solved = True

    __back_helper(board)
    return board
