#
# 25.10.2020
# https://gannett-hscp.blogspot.com/2020/05/
#

from z3 import *

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(4)]
     for i in range(4)]


def g15():
    init_state = ((1, 2, 3, 4),
                  (5, 6, 7, 8),
                  (9, 10, 12, 0),
                  (13, 14, 11, 15))

    final_state = ((1, 2, 3, 4),
                   (5, 6, 7, 8),
                   (9, 10, 11, 12),
                   (13, 14, 15, 0))

    cells_c = [And(0 <= X[i][j], X[i][j] <= 15) for i in range(4) for j in range(4)]
    distinct_c = [Distinct([X[i][j] for i in range(4) for j in range(4)])]
    final_state_c = [X[i][j] == final_state[i][j] for i in range(4) for j in range(4)]
    # c_state = [If(init_state[i][j] == 0, True, X[i][j] == init_state[i][j])
    #           for i in range(4) for j in range(4)]

    s = Solver()
    s.add(cells_c + distinct_c + final_state_c)
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)
        v = [[m.evaluate(X[i][j]) for j in range(4)]
             for i in range(4)]
        print(v)


def move_down(row, col):
    if row < 3:
        X[row + 1, col] = X[row, col]
        X[row, col] = 0
        return True
    else:
        return False


def move_up(row, col):
    if row > 0:
        X[row - 1, col] = X[row, col]
        X[row, col] = 0
        return True
    else:
        return False


def move_left(row, col):
    if col > 0:
        X[row, col - 1] = X[row, col]
        X[row, col] = 0
        return True
    else:
        return False


def move_right(row, col):
    if col < 3:
        X[row, col + 1] = X[row, col]
        X[row, col] = 0
        return True
    else:
        return False


def move_check(state, col_a, col_b):
    if len(state[col_a]) == 0:
        return False
    if len(state[col_b]) > 0:
        return min(state[col_a]) < min(state[col_b])
    else:
        return True


def move_op(state, col_a, col_b):
    if move_check(state, col_a, col_b):
        el = min(state[col_a])
        state[col_a].remove(el)
        state[col_b].append(el)


def move(state, op):
    return If(op == 0, move_op(state, 0, 1),
              If(op == 1, move_op(state, 1, 0),
                 If(op == 2, move_op(state, 0, 2),
                    If(op == 3, move_op(state, 2, 0),
                       If(op == 4, move_op(state, 1, 2),
                          move_op(state, 2, 1))))))


if __name__ == '__main__':
    set_param('parallel.enable', True)
    g15()
