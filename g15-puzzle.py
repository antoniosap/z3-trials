#
# 25.10.2020
# https://gannett-hscp.blogspot.com/2020/05/
#

import tkinter as tk
from z3 import *

BOARDS = 3

X = [[[Int("x_r%s_c%s_t%s" % (i + 1, j + 1, t + 1))
       for j in range(4)]
      for i in range(4)]
     for t in range(BOARDS)]

init_state = ((1, 2, 3, 4),
              (5, 6, 7, 8),
              (9, 10, 11, 0),
              (13, 14, 15, 12))

final_state = ((1, 2, 3, 4),
               (5, 6, 7, 8),
               (9, 10, 11, 12),
               (13, 14, 15, 0))

current_state = [[init_state[i][j] for j in range(4)] for i in range(4)]


def g15():
    set_param('parallel.enable', True)
    set_param('proof', True)
    set_param(verbose=1)
    z3.enable_trace('sat')
    cells_c = [And(0 <= X[t][i][j], X[t][i][j] <= 15) for j in range(4) for i in range(4) for t in range(BOARDS)]
    distinct_c = []
    for t in range(BOARDS):
        distinct_c.append(Distinct([X[t][i][j] for i in range(4) for j in range(4)]))
    final_state_c = [X[BOARDS - 1][i][j] == final_state[i][j] for i in range(4) for j in range(4)]
    init_state_c = [X[0][i][j] == init_state[i][j] for i in range(4) for j in range(4)]
    op = [Int('op_%d' % t) for t in range(BOARDS - 1)]
    op_c = [And(1 <= op[t], op[t] <= 2) for t in range(BOARDS - 1)]
    # moves_c = [X[t - 1][i][j] == move_tile(op[t], t, i, j) for i in range(4) for j in range(4) for t in range(BOARDS - 1)]
    # moves_c = [Or(move_down(1, 2, 3), move_up(1, 2, 3), move_right(1, 2, 3))]
    # moves_c = move_down(1, 2, 3)
    moves_c = []
    # le tessere senza il buco e senza buchi nell intorno, non si muovono
    fixed_c = []
    for t in range(BOARDS - 1):
        # quadrante NWW
        #   | 0  1  2  3
        # --|-----------
        # 0 | 1, 2, _, _
        # 1 | 5, 6, _, _
        # 2 | _, _, _, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][0] > 0, X[t + 1][0][0] > 0,
                              X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][1][0] > 0, X[t + 1][1][0] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0),
                          And(X[t][0][0] == X[t + 1][0][0],  # then
                              X[t][0][1] == X[t + 1][0][1],
                              X[t][1][0] == X[t + 1][1][0],
                              X[t][1][1] == X[t + 1][1][1]),
                          True))  # else
        # quadrante NW
        #   | 0  1  2  3
        # --|-----------
        # 0 | 1, 2, 3, _
        # 1 | 5, 6, 7, _
        # 2 | _, _, _, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][0] > 0, X[t + 1][0][0] > 0,
                              X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][0][2] > 0, X[t + 1][0][2] > 0,
                              X[t][1][0] > 0, X[t + 1][1][0] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0),
                          And(X[t][0][0] == X[t + 1][0][0],  # then
                              X[t][0][1] == X[t + 1][0][1],
                              X[t][0][2] == X[t + 1][0][2],
                              X[t][1][0] == X[t + 1][1][0],
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][1][2] == X[t + 1][1][2]),
                          True))  # else
        # quadrante NE
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, 2, 3, 4
        # 1 | _, 6, 7, 8
        # 2 | _, _, _, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][0][2] > 0, X[t + 1][0][2] > 0,
                              X[t][0][3] > 0, X[t + 1][0][3] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][1][3] > 0, X[t + 1][1][3] > 0),
                          And(X[t][0][1] == X[t + 1][0][1],  # then
                              X[t][0][2] == X[t + 1][0][2],
                              X[t][0][3] == X[t + 1][0][3],
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][1][3] == X[t + 1][1][3]),
                          True))  # else
        # quadrante NEE
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, 3, 4
        # 1 | _, _, 7, 8
        # 2 | _, _, _, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][2] > 0, X[t + 1][0][2] > 0,
                              X[t][0][3] > 0, X[t + 1][0][3] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][1][3] > 0, X[t + 1][1][3] > 0),
                          And(X[t][0][2] == X[t + 1][0][2],  # then
                              X[t][0][3] == X[t + 1][0][3],
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][1][3] == X[t + 1][1][3]),
                          True))  # else
        # quadrante CEE
        #   | 0  1  2  3
        # --|-----------
        # 0 | 1, 2, _, _
        # 1 | 5, 6, _, _
        # 2 | 9,10, _, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][0] > 0, X[t + 1][0][0] > 0,
                              X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][1][0] > 0, X[t + 1][1][0] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][2][0] > 0, X[t + 1][2][0] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0),
                          And(X[t][0][0] == X[t + 1][0][0],  # then
                              X[t][0][1] == X[t + 1][0][1],
                              X[t][1][0] == X[t + 1][1][0],
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][2][0] == X[t + 1][2][0],
                              X[t][2][1] == X[t + 1][2][1]),
                          True))  # else
        # quadrante CE
        #   | 0  1  2  3
        # --|-----------
        # 0 | 1, 2, 3, _
        # 1 | 5, 6, 7, _
        # 2 | 9,10,11, _
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][0] > 0, X[t + 1][0][0] > 0,
                              X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][0][2] > 0, X[t + 1][0][2] > 0,
                              X[t][1][0] > 0, X[t + 1][1][0] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][2][0] > 0, X[t + 1][2][0] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0),
                          And(X[t][0][0] == X[t + 1][0][0],  # then
                              X[t][0][1] == X[t + 1][0][1],
                              X[t][0][2] == X[t + 1][0][2],
                              X[t][1][0] == X[t + 1][1][0],
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][2][0] == X[t + 1][2][0],
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][2][2] == X[t + 1][2][2]),
                          True))  # else
        # quadrante CW
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, 2, 3, 4
        # 1 | _, 6, 7, 8
        # 2 | _,10,11,12
        # 3 | _, _, _, _
        fixed_c.append(If(And(X[t][0][1] > 0, X[t + 1][0][1] > 0,
                              X[t][0][2] > 0, X[t + 1][0][2] > 0,
                              X[t][0][3] > 0, X[t + 1][0][3] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][1][3] > 0, X[t + 1][1][3] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][2][3] > 0, X[t + 1][2][3] > 0),
                          And(X[t][0][1] == X[t + 1][0][1],  # then
                              X[t][0][2] == X[t + 1][0][2],
                              X[t][0][3] == X[t + 1][0][3],
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][1][3] == X[t + 1][1][3],
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][2][2] == X[t + 1][2][2],
                              X[t][2][3] == X[t + 1][2][3]),
                          True))  # else
        # quadrante SE
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | 5, 6, 7, _
        # 2 | 9,10,11, _
        # 3 |13,14,15, _
        fixed_c.append(If(And(X[t][1][0] > 0, X[t + 1][1][0] > 0,
                              X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][2][0] > 0, X[t + 1][2][0] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][3][0] > 0, X[t + 1][3][0] > 0,
                              X[t][3][1] > 0, X[t + 1][3][1] > 0,
                              X[t][3][2] > 0, X[t + 1][3][2] > 0),
                          And(X[t][1][0] == X[t + 1][1][0],  # then
                              X[t][1][1] == X[t + 1][1][1],
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][2][0] == X[t + 1][2][0],
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][2][2] == X[t + 1][2][2],
                              X[t][3][0] == X[t + 1][3][0],
                              X[t][3][1] == X[t + 1][3][1],
                              X[t][3][2] == X[t + 1][3][2]),
                          True))  # else
        # quadrante SW
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | _, 6, 7, 8
        # 2 | _,10,11,12
        # 3 | _,14,15,16
        fixed_c.append(If(And(X[t][1][1] > 0, X[t + 1][1][1] > 0,
                              X[t][1][2] > 0, X[t + 1][1][2] > 0,
                              X[t][1][3] > 0, X[t + 1][1][3] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][2][3] > 0, X[t + 1][2][3] > 0,
                              X[t][3][1] > 0, X[t + 1][3][1] > 0,
                              X[t][3][2] > 0, X[t + 1][3][2] > 0,
                              X[t][3][3] > 0, X[t + 1][3][3] > 0),
                          And(X[t][1][1] == X[t + 1][1][1],  # then
                              X[t][1][2] == X[t + 1][1][2],
                              X[t][1][3] == X[t + 1][1][3],
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][2][2] == X[t + 1][2][2],
                              X[t][2][3] == X[t + 1][2][3],
                              X[t][3][1] == X[t + 1][3][1],
                              X[t][3][2] == X[t + 1][3][2],
                              X[t][3][3] == X[t + 1][3][3]),
                          True))  # else
        # quadrante SWW
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | _, _, _, _
        # 2 | 9,10, _, _
        # 3 |13,14, _, _
        fixed_c.append(If(And(X[t][2][0] > 0, X[t + 1][2][0] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][3][0] > 0, X[t + 1][3][0] > 0,
                              X[t][3][1] > 0, X[t + 1][3][1] > 0),
                          And(X[t][2][0] == X[t + 1][2][0],  # then
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][3][0] == X[t + 1][3][0],
                              X[t][3][1] == X[t + 1][3][1]),
                          True))  # else
        # # quadrante SW
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | _, _, _, _
        # 2 | 9,10,11, _
        # 3 |13,14,15, _
        fixed_c.append(If(And(X[t][2][0] > 0, X[t + 1][2][0] > 0,
                              X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][3][0] > 0, X[t + 1][3][0] > 0,
                              X[t][3][1] > 0, X[t + 1][3][1] > 0,
                              X[t][3][2] > 0, X[t + 1][3][2] > 0),
                          And(X[t][2][0] == X[t + 1][2][0],  # then
                              X[t][2][1] == X[t + 1][2][1],
                              X[t][2][2] == X[t + 1][2][2],
                              X[t][3][0] == X[t + 1][3][0],
                              X[t][3][1] == X[t + 1][3][1],
                              X[t][3][2] == X[t + 1][3][2]),
                          True))  # else
        # # quadrante SE
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | _, _, _, _
        # 2 | _,10,11,12
        # 3 | _,14,15,16
        fixed_c.append(If(And(X[t][2][1] > 0, X[t + 1][2][1] > 0,
                              X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][2][3] > 0, X[t + 1][2][3] > 0,
                              X[t][3][1] > 0, X[t + 1][3][1] > 0,
                              X[t][3][2] > 0, X[t + 1][3][2] > 0,
                              X[t][3][3] > 0, X[t + 1][3][3] > 0),
                          And(X[t][2][1] == X[t + 1][2][1],  # then
                              X[t][2][2] == X[t + 1][2][2],
                              X[t][2][3] == X[t + 1][2][3],
                              X[t][3][1] == X[t + 1][3][1],
                              X[t][3][2] == X[t + 1][3][2],
                              X[t][3][3] == X[t + 1][3][3]),
                          True))  # else
        # # quadrante SEE
        #   | 0  1  2  3
        # --|-----------
        # 0 | _, _, _, _
        # 1 | _, _, _, _
        # 2 | _, _,11,12
        # 3 | _, _,15,16
        fixed_c.append(If(And(X[t][2][2] > 0, X[t + 1][2][2] > 0,
                              X[t][2][3] > 0, X[t + 1][2][3] > 0,
                              X[t][3][2] > 0, X[t + 1][3][2] > 0,
                              X[t][3][3] > 0, X[t + 1][3][3] > 0),
                          And(X[t][2][2] == X[t + 1][2][2],  # then
                              X[t][2][3] == X[t + 1][2][3],
                              X[t][3][2] == X[t + 1][3][2],
                              X[t][3][3] == X[t + 1][3][3]),
                          True))  # else

    # le tessere blank => swap con solo una adiacente
    MOVE_NULL, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN = 'NULL', 'LEFT', 'RIGHT', 'UP', 'DOWN'
    move_name = [MOVE_NULL, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN]
    move = {k: v for k, v in zip(move_name, range(len(move_name)))}
    cell_pos = [(-1, -1)] + [(i, j) for i in range(4) for j in range(4)]

    def cell_x(tt, pos):
        i, j = cell_pos[pos]
        return X[tt][i][j]

    def cell_fixed(tt, pos_list):
        return And([cell_x(tt + 1, pos) == cell_x(tt, pos) for pos in pos_list])

    def cell_swap_x(tt, pos_t1, pos_t0):
        return And(cell_x(tt + 1, pos_t1) == cell_x(tt, pos_t0), cell_x(tt + 1, pos_t0) == cell_x(tt, pos_t1))

    def cell_swap_move(tt, move_pos_name, pos_t1, pos_t0):
        print(f"cell_swap_move t {tt} {op[tt]}=={move_pos_name} {pos_t1} {pos_t0}")
        return Implies(op[tt] == move[move_pos_name], cell_swap_x(tt, pos_t1, pos_t0))

    def null_move(tt):
        return If(op[tt] == move[MOVE_NULL], True, True)

    # TODO factorize + generalize su AST, abstract syntax tree, python ast
    cell_neighbors = {
        1: {MOVE_DOWN: 5, MOVE_RIGHT: 2},
        2: {MOVE_LEFT: 1, MOVE_DOWN: 6, MOVE_RIGHT: 3},
        3: {MOVE_LEFT: 2, MOVE_DOWN: 7, MOVE_RIGHT: 4},
        4: {MOVE_DOWN: 8, MOVE_LEFT: 3},
        5: {MOVE_UP: 1, MOVE_DOWN: 9, MOVE_RIGHT: 6},
        6: {MOVE_LEFT: 5, MOVE_UP: 2, MOVE_DOWN: 10, MOVE_RIGHT: 7},
        7: {MOVE_LEFT: 6, MOVE_UP: 3, MOVE_DOWN: 11, MOVE_RIGHT: 8},
        8: {MOVE_LEFT: 7, MOVE_UP: 4, MOVE_DOWN: 12},
        9: {MOVE_RIGHT: 10, MOVE_UP: 5, MOVE_DOWN: 13},
        10: {MOVE_LEFT: 9, MOVE_UP: 6, MOVE_DOWN: 14, MOVE_RIGHT: 11},
        11: {MOVE_LEFT: 10, MOVE_UP: 7, MOVE_DOWN: 15, MOVE_RIGHT: 12},
        12: {MOVE_LEFT: 11, MOVE_UP: 8, MOVE_DOWN: 16},
        13: {MOVE_UP: 9, MOVE_RIGHT: 14},
        14: {MOVE_LEFT: 13, MOVE_UP: 10, MOVE_RIGHT: 15},
        15: {MOVE_LEFT: 14, MOVE_UP: 11, MOVE_RIGHT: 16},
        16: {MOVE_LEFT: 15, MOVE_UP: 12}
    }

    cell_zero_c = []
    for t in range(BOARDS - 1):
        # # quadrante SEE
        #   t 1                   t 0  op 1           t 0  op 2
        #   | 0  1  2  3          | 0  1  2  3        | 0  1  2  3
        # --|-----------        --|-----------      --|-----------
        # 0 | 1, 2, 3, 4        0 | 1, 2, 3, 4      0 | 1, 2, 3, 4
        # 1 | 5, 6, 7, 8  <--   1 | 5, 6, 7, 8      1 | 5, 6, 7, 8
        # 2 | 9,10,11,12        2 | 9,10,11,12      2 | 9,10,11,
        # 3 |13,14,15,          3 |13,14,  ,15      3 |13,14,15,12
        # cell_center = 16
        # cell_zero_c.append(If(cell_x(t + 1, cell_center) == 0,
        #                       AtMost(cell_swap_move(t, MOVE_LEFT, cell_center, cell_neighbors[cell_center][MOVE_LEFT]),
        #                              cell_swap_move(t, MOVE_UP, cell_center, cell_neighbors[cell_center][MOVE_UP]),
        #                              # null_move(t),
        #                              1),
        #                       True))
        cell_zero_c.append(Implies(cell_x(t + 1, 16) == 0,
                                   AtMost(cell_swap_move(t, MOVE_LEFT, 16, 15),
                                          cell_swap_move(t, MOVE_UP, 16, 12),
                                          # null_move(t),
                                          1),
                                   ))
        cell_zero_c.append(cell_fixed(t, (14, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)))

    s = Solver()
    s.add(cells_c + distinct_c + init_state_c + final_state_c + fixed_c + cell_zero_c + op_c)
    r = s.check()
    # print(s.assertions())
    # print(s.help())
    print(f"SOLUTION: {r}")
    if r == sat:
        # print("MODEL:")
        m = s.model()
        # print(m)
        print("BOARDS:")
        for t in range(BOARDS):
            print(f"BOARD t {t}")
            board = [[int(str(m.evaluate(X[t][i][j]))) for j in range(4)] for i in range(4)]
            g15_display(board)
        print("MOVES:")
        mv = [move_name[int(str(m[op[t]]))] for t in range(BOARDS - 1)]
        print(mv)
    else:
        pass
        # print(s.param_descrs())
        # print(s.sexpr())
        # print(s.help())
        # print(s.units())
        # print(s.assertions())
        # print(s.proof())


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


# ----------------------------------------------------------------------------------------------------

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


def g15_move_up(s):
    r, c = g15_find_hole(s)
    if r < 3:
        s[r][c] = s[r + 1][c]
        s[r + 1][c] = 0
    return s


def g15_move_left(s):
    r, c = g15_find_hole(s)
    if c < 3:
        s[r][c] = s[r][c + 1]
        s[r][c + 1] = 0
    return s


def g15_move_right(s):
    r, c = g15_find_hole(s)
    if c > 0:
        s[r][c] = s[r][c - 1]
        s[r][c - 1] = 0
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
        self.go_pad = tk.Button(self, text="*** GO ***", command=g15).pack(side="bottom")
        print(f"INITIAL STATE t 0")
        g15_display(init_state)
        print(f"FINAL STATE t {BOARDS - 1}")
        g15_display(final_state)

    def move_top(self):
        print("MOVE TOP")
        g15_move_up(current_state)
        g15_display(current_state)

    def move_bottom(self):
        print("MOVE BOTTOM")
        g15_move_down(current_state)
        g15_display(current_state)

    def move_left(self):
        print("MOVE LEFT")
        g15_move_left(current_state)
        g15_display(current_state)

    def move_right(self):
        print("MOVE RIGHT")
        g15_move_right(current_state)
        g15_display(current_state)


if __name__ == '__main__':
    print(f"Z3 version {z3.get_full_version()}")
    root = tk.Tk()
    root.geometry("+1000+100")
    root.title("SAT/SMT 15 puzzle")
    app = App(master=root)
    app.mainloop()
