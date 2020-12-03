#
# 25.10.2020
# https://gannett-hscp.blogspot.com/2020/05/
#

import tkinter as tk
from z3 import *

BOARDS = 10

X = [[[Int(f"P1_t{t}"), Int(f"P2_t{t}"), Int(f"P3_t{t}"), Int(f"P4_t{t}")],
      [Int(f"P5_t{t}"), Int(f"P6_t{t}"), Int(f"P7_t{t}"), Int(f"P8_t{t}")],
      [Int(f"P9_t{t}"), Int(f"P10_t{t}"), Int(f"P11_t{t}"), Int(f"P12_t{t}")],
      [Int(f"P13_t{t}"), Int(f"P14_t{t}"), Int(f"P15_t{t}"), Int(f"P16_t{t}")]]
     for t in range(BOARDS)]

init_state = ((5, 1, 2, 3),
              (6, 7, 0, 4),
              (9, 10, 11, 8),
              (13, 14, 15, 12))

final_state = ((1, 2, 3, 4),
               (5, 6, 7, 8),
               (9, 10, 11, 12),
               (13, 14, 15, 0))

current_state = [[final_state[i][j] for j in range(4)] for i in range(4)]


def g15():
    set_param('parallel.enable', True)
    set_param('proof', True)
    set_param(verbose=10)
    # z3_trace()

    cells_c = [And(0 <= X[t][i][j], X[t][i][j] <= 15) for j in range(4) for i in range(4) for t in range(BOARDS)]
    distinct_c = []
    for t in range(BOARDS):
        distinct_c.append(Distinct([X[t][i][j] for i in range(4) for j in range(4)]))
    final_state_c = [X[BOARDS - 1][i][j] == final_state[i][j] for i in range(4) for j in range(4)]
    init_state_c = [X[0][i][j] == init_state[i][j] for i in range(4) for j in range(4)]

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
    op = [Int('op_%d' % t) for t in range(BOARDS - 1)]
    op_c = [And(0 <= op[t], op[t] <= len(move_name) - 1) for t in range(BOARDS - 1)]

    def cell_x(tt, pos):
        i, j = cell_pos[pos]
        return X[tt][i][j]

    def cell_blank(tt, pos):
        return cell_x(tt, pos) == 0

    def cell_move_fixed(tt, cell_center):
        # print(f"cell_move_fixed: t={tt} c={cell_center} {cell_fixed[cell_center]}")
        return And([cell_x(tt + 1, pos) == cell_x(tt, pos) for pos in cell_fixed[cell_center]])

    def cell_swap_x(tt, pos_t1, pos_t0):
        return And(cell_x(tt + 1, pos_t1) == cell_x(tt, pos_t0), cell_x(tt + 1, pos_t0) == cell_x(tt, pos_t1))

    def cell_move_only_one(tt, cell_center):
        cell_neigh = []
        for cell in cell_movable[cell_center]:
            if cell != cell_center:
                cell_neigh.append(cell_swap_x(tt, cell, cell_center))
        return AtMost(*cell_neigh, 1)

    def cell_swap_move(tt, move_pos_name, pos_t1, pos_t0):
        # print(f"cell_swap_move: t={tt} if {op[tt]}=={move_pos_name} swap {pos_t1} {pos_t0}")
        return Implies(op[tt] == move[move_pos_name], cell_swap_x(tt, pos_t1, pos_t0))

    def null_move(tt):
        return If(op[tt] == move[MOVE_NULL], True, True)

    # TODO factorize + generalize su AST, abstract syntax tree, python ast
    cell_move = {
        # key = cell center
        0: {},
        1: {5: MOVE_UP, 2: MOVE_LEFT},  # ok
        2: {6: MOVE_UP, 1: MOVE_RIGHT, 3: MOVE_LEFT},  # ok
        3: {7: MOVE_UP, 2: MOVE_RIGHT, 4: MOVE_LEFT},  # ok
        4: {8: MOVE_UP, 3: MOVE_LEFT},  # ok
        5: {9: MOVE_UP, 1: MOVE_DOWN, 6: MOVE_LEFT},  # ok
        6: {10: MOVE_UP, 7: MOVE_LEFT, 2: MOVE_DOWN, 5: MOVE_RIGHT},  # ok
        7: {11: MOVE_UP, 3: MOVE_DOWN, 8: MOVE_LEFT, 6: MOVE_RIGHT},  # ok
        8: {12: MOVE_UP, 4: MOVE_DOWN, 7: MOVE_RIGHT},  # ok
        9: {10: MOVE_LEFT, 13: MOVE_UP, 5: MOVE_DOWN},  # ok
        10: {14: MOVE_UP, 11: MOVE_LEFT, 6: MOVE_DOWN, 9: MOVE_RIGHT},  # ok
        11: {15: MOVE_UP, 12: MOVE_LEFT, 7: MOVE_DOWN, 10: MOVE_RIGHT},  # ok
        12: {16: MOVE_UP, 8: MOVE_DOWN, 11: MOVE_RIGHT},  # ok
        13: {9: MOVE_DOWN, 14: MOVE_LEFT},  # ok
        14: {10: MOVE_DOWN, 13: MOVE_RIGHT, 15: MOVE_LEFT},  # ok
        15: {11: MOVE_DOWN, 14: MOVE_RIGHT, 16: MOVE_LEFT},  # ok
        16: {15: MOVE_RIGHT, 12: MOVE_DOWN}  # ok
    }

    def cell_out(cell_list_in):
        return [c for c in [*range(1, 4 * 4 + 1)] if c not in cell_list_in]

    cell_movable = {
        # key = cell center
        0: (),
        1: (1, 2, 5),
        2: (1, 2, 3, 6),
        3: (2, 3, 4, 7),
        4: (3, 4, 8),
        5: (1, 5, 6, 9),
        6: (2, 6, 5, 7, 10),
        7: (3, 6, 7, 8, 11),
        8: (4, 7, 8, 12),
        9: (5, 9, 10, 13),
        10: (6, 9, 10, 11, 14),
        11: (7, 10, 11, 12, 14),
        12: (8, 11, 12, 15),
        13: (9, 13, 14),
        14: (10, 13, 14, 15),
        15: (11, 14, 15, 16),
        16: (12, 14, 15)
    }

    cell_fixed = {
        # key = cell center
        0: (),
        1: cell_out(cell_movable[1]),
        2: cell_out(cell_movable[2]),
        3: cell_out(cell_movable[3]),
        4: cell_out(cell_movable[4]),
        5: cell_out(cell_movable[5]),
        6: cell_out(cell_movable[6]),
        7: cell_out(cell_movable[7]),
        8: cell_out(cell_movable[8]),
        9: cell_out(cell_movable[9]),
        10: cell_out(cell_movable[10]),
        11: cell_out(cell_movable[11]),
        12: cell_out(cell_movable[12]),
        13: cell_out(cell_movable[13]),
        14: cell_out(cell_movable[14]),
        15: cell_out(cell_movable[15]),
        16: cell_out(cell_movable[16])
    }

    # --> intorno di P
    cell_zero_c = []
    for t in range(BOARDS - 1):
        cell_zero_c.append(op[t] != move[MOVE_NULL])
        for cell_center in range(1, 4 * 4 + 1):
            for cell in cell_move[cell_center]:
                cell_move_from = cell_move[cell_center][cell]
                cell_zero_c.append(Implies(And(cell_blank(t, pos=cell_center),
                                               cell_x(t, pos=cell_center) == cell_x(t + 1, pos=cell),
                                               # cercare la cella bianca e fissare tutte le altre
                                               cell_move_fixed(t, cell_center=cell_center)
                                               ),
                                           And(cell_blank(t + 1, pos=cell),
                                               op[t] == move[cell_move_from])
                                           )
                                   )

    # muovere una sola cella (cioè uno swap, quindi 2) ad ogni t
    cell_move_one = []
    for t in range(BOARDS - 1):
        c = []
        for cell in range(1, 4 * 4 + 1):
            c.append(cell_x(t + 1, cell) != cell_x(t, cell))
        cell_move_one.append(AtMost(*c, 2))
        cell_move_one.append(AtLeast(*c, 2))

    # la cella blank si deve spostare ad ogni board, non puo rimanere fissa
    cell_blank_move_one = []
    for t in range(BOARDS - 1):
        c = []
        for cell in range(1, 4 * 4 + 1):
            c.append(Implies(cell_x(t, cell) == 0, cell_x(t + 1, cell) != 0))
        cell_blank_move_one.append(And(*c))

    s = Solver()
    s.add(cells_c + distinct_c + init_state_c + final_state_c + fixed_c + cell_zero_c + op_c + cell_move_one + cell_blank_move_one)
    r = s.check()
    # print(s.assertions())
    # print(s.help())
    # print(s.to_smt2())
    # print(s.units())
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
    print("| P1 | P2 | P3 | P4 |")
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[1][0], s[1][1], s[1][2], s[1][3]).replace(' 0 ', '   '))
    print("| P5 | P6 | P7 | P8 |")
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[2][0], s[2][1], s[2][2], s[2][3]).replace(' 0 ', '   '))
    print("| P9 |P10 |P11 |P12 |")
    print("|----|----|----|----|")
    print("| {:2d} | {:2d} | {:2d} | {:2d} |".format(s[3][0], s[3][1], s[3][2], s[3][3]).replace(' 0 ', '   '))
    print("|P13 |P14 |P15 |P16 |")
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


def z3_trace():
    z3.enable_trace('sat')
    z3.enable_trace('goal')
    z3.enable_trace('ackermannize')
    z3.enable_trace('model_constructor')
    z3.enable_trace('z3_replayer')
    z3.enable_trace('algebraic2expr')
    z3.enable_trace('pp_ast_dot_step')
    z3.enable_trace('smt2_pp')
    z3.enable_trace('pp_let')
    z3.enable_trace('pp_scope')
    z3.enable_trace('ast_translation')
    z3.enable_trace('ast')
    z3.enable_trace('mk_modus_ponens')
    z3.enable_trace('mk_transitivity')
    z3.enable_trace('distinct')
    z3.enable_trace('unit_resolution')
    z3.enable_trace('datatype')
    z3.enable_trace('euf')
    z3.enable_trace('nnf')
    z3.enable_trace('pattern_inference')
    z3.enable_trace('proof_checker')
    z3.enable_trace('rewriter')
    z3.enable_trace('seq')
    z3.enable_trace('seq_verbose')
    z3.enable_trace('unifier')
    z3.enable_trace('grobner')
    z3.enable_trace('dd.solver')
    z3.enable_trace('grobner_d')
    z3.enable_trace('nla_solver')
    z3.enable_trace('model')
    z3.enable_trace('opt')
    z3.enable_trace('sat_tactic')
    z3.enable_trace('model_checker')


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
        self.planned_boards = 1

    def move_top(self):
        self.planned_boards += 1
        print(f"MOVE TOP (set BOARDS to: {self.planned_boards})")
        g15_move_up(current_state)
        g15_display(current_state)

    def move_bottom(self):
        self.planned_boards += 1
        print(f"MOVE BOTTOM (set BOARDS to: {self.planned_boards})")
        g15_move_down(current_state)
        g15_display(current_state)

    def move_left(self):
        self.planned_boards += 1
        print(f"MOVE LEFT (set BOARDS to: {self.planned_boards})")
        g15_move_left(current_state)
        g15_display(current_state)

    def move_right(self):
        self.planned_boards += 1
        print(f"MOVE RIGHT (set BOARDS to: {self.planned_boards})")
        g15_move_right(current_state)
        g15_display(current_state)


if __name__ == '__main__':
    print(f"Z3 version {z3.get_full_version()}")
    root = tk.Tk()
    root.geometry("+1000+100")
    root.title("SAT/SMT 15 puzzle")
    app = App(master=root)
    app.mainloop()
