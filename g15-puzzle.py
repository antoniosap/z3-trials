#
# 25.10.2020
# https://gannett-hscp.blogspot.com/2020/05/
#

import tkinter as tk
from z3 import *

BOARDS = 2
MOVE_DOWN, MOVE_UP, MOVE_LEFT, MOVE_RIGHT = 0, 1, 2, 3

X = [[[Int("x_r%s_c%s_t%s" % (i + 1, j + 1, k + 1))
       for j in range(4)]
      for i in range(4)]
     for k in range(BOARDS)]

init_state = ((1, 2, 3, 4),
              (5, 6, 7, 8),
              (9, 10, 12, 0),
              (13, 14, 11, 15))

final_state = ((1, 2, 3, 4),
               (5, 6, 7, 8),
               (9, 10, 11, 12),
               (13, 14, 15, 0))

current_state = [[init_state[i][j] for j in range(4)] for i in range(4)]


def g15():
    cells_c = [And(0 <= X[k][i][j], X[k][i][j] <= 15) for j in range(4) for i in range(4) for k in range(BOARDS)]
    distinct_c = [Distinct([X[k][i][j] for i in range(4) for j in range(4) for k in range(BOARDS)])]
    final_state_c = [X[0][i][j] == final_state[i][j] for i in range(4) for j in range(4)]
    init_state_c = [X[BOARDS - 1][i][j] == init_state[i][j] for i in range(4) for j in range(4)]
    op = [Int('op_%d' % n) for n in range(BOARDS - 1)]
    moves_c = [X[k - 1][i][j] == move_tile(op[k], X, i, j) for i in range(4) for j in range(4) for k in range(BOARDS)]

    s = Solver()
    s.add(cells_c + distinct_c + init_state_c + final_state_c + moves_c)
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)
        ev = [[[m.evaluate(X[k][i][j]) for j in range(4)]
               for i in range(4)]
              for k in range(BOARDS)]
        print(ev)


def move_null():
    return []


def move_down(board, row, col):
    def move(board, row, col):
        return [X[board - 1][row + 1][col] == X[board][row][col], X[board - 1][row][col] == 0]

    if board > 0 and row < 3:
        return [If(X[board - 1][row + 1][col] == 0, move(board, row, col), [])]
    else:
        return []


def move_up(board, row, col):
    def move(board, row, col):
        return [X[board - 1][row - 1][col] == X[board][row][col], X[board - 1][row][col] == 0]

    if board > 0 and row > 0:
        return [If(X[board - 1][row - 1][col] == 0, move(board, row, col), [])]
    else:
        return []


def move_left(board, row, col):
    def move(board, row, col):
        return [X[board - 1][row][col - 1] == X[board][row][col], X[board - 1][row][col] == 0]

    if board > 0 and col > 0:
        return [If(X[board - 1][row][col - 1] == 0, move(board, row, col), [])]
    else:
        return []


def move_right(board, row, col):
    def move(board, row, col):
        return [X[board - 1][row][col + 1] == X[board][row][col], X[board - 1][row][col] == 0]

    if board > 0 and col < 3:
        return [If(X[board - 1][row][col + 1] == 0, move(board, row, col), [])]
    else:
        return []


def move_tile(op, board, row, col):
    return If(op == MOVE_DOWN, move_down(board, row, col),
              If(op == MOVE_UP, move_up(board, row, col),
                 If(op == MOVE_LEFT, move_left(board, row, col),
                    If(op == MOVE_RIGHT, move_right(board, row, col),
                       move_null()))))


def g15_display(s):
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[0][0], s[0][1], s[0][2], s[0][3]).replace(' 0 ', '   '))
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[1][0], s[1][1], s[1][2], s[1][3]).replace(' 0 ', '   '))
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[2][0], s[2][1], s[2][2], s[2][3]).replace(' 0 ', '   '))
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[3][0], s[3][1], s[3][2], s[3][3]).replace(' 0 ', '   '))
    print("|----|----|----|----|")
    print()


def g15_find_hole(s):
    for r in range(4):
        for c in range(4):
            if s[r][c] == 0:
                return r, c


def g15_move_down(s):
    r, c = g15_find_hole(s)
    if r > 0:
        s[r][c] = s[r - 1][c]
        s[r - 1][c] = 0
    return s


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.top_pad = tk.Button(self, text="TOP\n|||", command=self.move_top).pack(side="top")
        self.left_pad = tk.Button(self, text="L <--", command=self.move_left).pack(side="left")
        self.right_pad = tk.Button(self, text="--> R", command=self.move_right).pack(side="right")
        self.bot_pad = tk.Button(self, text="|||\nBOT", command=self.move_bottom).pack(side="bottom")
        g15_display(current_state)

    def move_top(self):
        print("MOVE TOP")
        g15_display(current_state)

    def move_bottom(self):
        print("MOVE BOTTOM")
        g15_move_down(current_state)
        g15_display(current_state)

    def move_left(self):
        print("MOVE LEFT")
        g15_display(current_state)

    def move_right(self):
        print("MOVE RIGHT")
        g15_display(current_state)


if __name__ == '__main__':
    set_param('parallel.enable', True)
    # g15()
    root = tk.Tk()
    root.geometry("+1000+100")
    app = App(master=root)
    app.mainloop()
