#
# 25.10.2020
# https://gannett-hscp.blogspot.com/2020/05/
#

from z3 import *

BOARDS = 2
MOVE_DOWN, MOVE_UP, MOVE_LEFT, MOVE_RIGHT = 0, 1, 2, 3

X = [[[Int("x_r%s_c%s_t%s" % (i + 1, j + 1, k + 1))
       for j in range(4)]
      for i in range(4)]
     for k in range(BOARDS)]


def g15():
    init_state = ((1, 2, 3, 4),
                  (5, 6, 7, 8),
                  (9, 10, 12, 0),
                  (13, 14, 11, 15))

    final_state = ((1, 2, 3, 4),
                   (5, 6, 7, 8),
                   (9, 10, 11, 12),
                   (13, 14, 15, 0))

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


if __name__ == '__main__':
    set_param('parallel.enable', True)
    g15()
