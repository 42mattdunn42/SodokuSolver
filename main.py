"""
The GUI and all other aspects of the sodoku game.
The board state will be loaded in from a csv.
"""

from tkinter import *
import csv
import solver


def validate(P):
    if len(P) == 0:
        # empty Entry is ok
        return True
    elif len(P) == 1 and P.isdigit():
        # Entry with 1 digit is ok
        return True
    else:
        # Anything else, reject it
        return False


def main():
    global board_state, board

    def populate_board(state):
        for i in range(9):
            for k in range(9):
                if state[i][k].isdigit():
                    board_state[k][i].insert(0, state[i][k])
    
    def clear_all():
        for i in range(9):
            for k in range(9):
                board_state[k][i].delete(0, 'end')
    
    def clear_entries():
        global board
        clear_all()
        populate_board(board)

    def get_current_state():
        curr_state = []
        for i in range(9):
            temp = []
            for k in range(9):
                temp.append(board_state[k][i].get())
            curr_state.append(temp)
            del temp
        return curr_state

    def btrack():
        solution = solver.backtracking(get_current_state())
        populate_board(solution)

    def open_popup(message):
        top= Toplevel(root)
        top.title("Status")
        Label(top, text=message).grid(row=0, column=0)

    def check_if_solved(event=None):
        # Get current board state
        curr_state = get_current_state()

        # try statement is to catch any non-filled in spots
        try:
            # Check if every row is valid
            for i in range(9):
                check = [0] * 10
                for k in range(9):
                    check[int(curr_state[i][k])] += 1
                if check[0] > 0:
                    open_popup("Not a solution, no zeros allowed.")
                    return
                else:
                    check.pop(0)
                    if not all(x == 1 for x in check):
                        open_popup("Not a solution. Duplicate found in row.")
                        return
            
            # Check if every column is valid
            for k in range(9):
                check = [0] * 10
                for i in range(9):
                    check[int(curr_state[i][k])] += 1
                check.pop(0)
                if not all(x == 1 for x in check):
                    open_popup("Not a solution. Duplicate found in column.")
                    return
            
            # Check if every box is valid
            for x in range(0, 9, 3):
                for y in range(0, 9, 3):
                    check = [0] * 10
                    for i in range(x, x + 3):
                        for k in range(y, y + 3):
                            check[int(curr_state[i][k])] += 1
                    check.pop(0)
                    if not all(x == 1 for x in check):
                        open_popup("Not a solution. Duplicate found in box.")
                        return

        except ValueError:
            open_popup("Not a solution, all places must be filled out.")
            return
        
        open_popup("Congratulations! This is a solution.")
        return

    def save(event=None):
        out = []
        for i in range(9):
            temp = []
            for k in range(9):
                temp.append(board_state[k][i].get())
            out.append(temp)
            del temp
        with open("board.csv", 'w', newline='') as f:
            csv_file = csv.writer(f)
            csv_file.writerows(out)
        f.close()
        del out

    # Read in csv
    board = []
    try:
        with open("board.csv", 'r') as f:
            csv_file = csv.reader(f)
            for row in csv_file:
                board.append(row)
        f.close()
    except FileNotFoundError:
        pass
    # Makes sure board has the correct demensions
    total = 0
    for i in range(len(board)):
        for k in range(len(board[i])):
            total += 1
    if total != 81:
        board = []
        for i in range(9):
            temp = []
            for k in range(9):
                temp.append('')
            board.append(temp)
            del temp
    del total

    # Create board
    board_state = []
    root = Tk()
    for k in range(11):
        temp = []
        for i in range(11):
            if i == 3 and (k == 3 or k == 7) or i == 7 and (k == 3 or k == 7):
                t = Label(root, text="+")
                t.grid(row=k, column=i, padx=5, pady=5)
            elif i == 3 or i == 7:
                t = Label(root, text="|")
                t.grid(row=k, column=i, padx=5, pady=5)
            elif k == 3 or k == 7:
                t = Label(root, text="-")
                t.grid(row=k, column=i, padx=5, pady=5)
            else:
                vcmd = (root.register(validate), '%P')
                curr = Entry(root, width=1, validate="key", validatecommand=vcmd)
                curr.grid(row=k, column=i, padx=5, pady=5)
                temp.append(curr)
        if len(temp) != 0:
            board_state.append(temp)
        del temp

    # Populate board
    populate_board(board)
    
    # Create menus
    menu_bar = Menu(root)
    # Save Menu
    board_menu = Menu(menu_bar, tearoff=0)
    board_menu.add_command(label="Save", command=save, accelerator="Ctrl+S")
    board_menu.add_separator()
    board_menu.add_command(label='Restart', command=clear_entries)
    board_menu.add_command(label='Clear All', command=clear_all)
    menu_bar.add_cascade(label="Board", menu=board_menu)
    # Solve Menu
    solve_menu = Menu(menu_bar,tearoff=0)
    solve_menu.add_command(label='Check Solution', command=check_if_solved, accelerator="Ctrl+D")
    solve_menu.add_separator()
    # Add commands for different solving algos here
    solve_menu.add_command(label='Backtracking', command=btrack)
    menu_bar.add_cascade(label="Solve", menu=solve_menu)
    
    root.title("Sodoku")
    root.config(menu=menu_bar)
    root.bind("<Control-s>", save)
    root.bind("<Control-d>", check_if_solved)
    root.mainloop()


if __name__ == "__main__":
    main()
