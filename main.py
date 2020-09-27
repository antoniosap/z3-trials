# 23.9.2020

from z3 import *


def sodoku():
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(9)]
         for i in range(9)]
    cells_c = [And(1 <= X[i][j], X[i][j] <= 9)
               for i in range(9) for j in range(9)]
    rows_c = [Distinct(X[i]) for i in range(9)]
    cols_c = [Distinct([X[i][j] for i in range(9)])
              for j in range(9)]
    sq_c = [Distinct([X[3 * i0 + i][3 * j0 + j]
                      for i in range(3) for j in range(3)])
            for i0 in range(3) for j0 in range(3)]
    sudoku_c = cells_c + rows_c + cols_c + sq_c
    instance = ((0, 0, 0, 0, 9, 4, 0, 3, 0),
                (0, 0, 0, 5, 1, 0, 0, 0, 7),
                (0, 8, 9, 0, 0, 0, 0, 4, 0),
                (0, 0, 0, 0, 0, 0, 2, 0, 8),
                (0, 6, 0, 2, 0, 1, 0, 5, 0),
                (1, 0, 2, 0, 0, 0, 0, 0, 0),
                (0, 7, 0, 0, 0, 0, 5, 2, 0),
                (9, 0, 0, 0, 6, 5, 0, 0, 0),
                (0, 4, 0, 9, 7, 0, 0, 0, 0))
    instance_c = [If(instance[i][j] == 0,
                     True,
                     X[i][j] == instance[i][j])
                  for i in range(9) for j in range(9)]
    s = Solver()
    s.add(sudoku_c + instance_c)
    s.check()
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(9)]
         for i in range(9)]
    print_matrix(r)


def tc_r():
    A = IntSort()
    B = BoolSort()
    R = Function('R', A, A, B)
    TC_R = TransitiveClosure(R)


def tr():
    B = BoolSort()
    s = Solver()
    G = DeclareSort('G')
    R = Function('R', G, G, B)
    x, y, z = Consts('x y z', G)
    a1, a2, a3, a4 = Consts('a1 a2 a3 a4', G)
    s.add(ForAll([x], R(x, x)))
    s.add(ForAll([x, y], Implies(And(R(x, y), R(y, x)), x == y)))
    s.add(ForAll([x, y, z], Implies(And(R(x, y), R(y, z)), R(x, z))))
    #
    s.add(R(a1, a2), R(a3, a4))
    # solution
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)


def move_check(state: list, col_a: int, col_b: int) -> bool:
    if len(state[col_a]) == 0:
        return False
    if len(state[col_b]) > 0:
        return min(state[col_a]) < min(state[col_b])
    else:
        return True


def move_op(state: list, col_a: int, col_b: int) -> None:
    if move_check(state, col_a, col_b):
        el = min(state[col_a])
        state[col_a].remove(el)
        state[col_b].append(el)


move_names = ["MOVE 1 -> 2", "MOVE 2 -> 1",
              "MOVE 1 -> 3", "MOVE 3 -> 1",
              "MOVE 2 -> 3", "MOVE 3 -> 2"]


def move(state: list, op: int):
    return If(op == 0, move_op(state, 0, 1),
              If(op == 1, move_op(state, 1, 0),
                 If(op == 2, move_op(state, 0, 2),
                    If(op == 3, move_op(state, 2, 0),
                       If(op == 4, move_op(state, 1, 2),
                          move_op(state, 2, 1))))))


def hanoi():
    s = Solver()
    stack = [[1, 2, 3, 4], [], []]
    goal = [[], [1, 2, 3, 4], []]
    # state spaces
    L = BitVec('L', 4)  # left
    C = BitVec('C', 4)  # center
    R = BitVec('R', 4)  # right
    # init state
    for i in range(4):
        if i in stack[0]:
            L |= 2**i
        if i in stack[1]:
            C |= 2**i
        if i in stack[2]:
            R |= 2**i
    #
    # solution
    #r = s.check()
    #print(r)
    #if r == sat:
    #    m = s.model()
    #    print(m)


def alphametics():
    # VIOLIN + VIOLIN + VIOLA = TRIO + SONATA
    A, I, L, N, O, R, S, T, V = Ints('A, I, L, N, O, R, S, T, V')
    s = Solver()
    s.add( Distinct (A, I, L, N, O, R, S, T, V))
    s.add(And(A >= 0, A <= 9))
    s.add(And(I >= 0, I <= 9))
    s.add(And(L >= 0, L <= 9))
    s.add(And(N >= 0, N <= 9))
    s.add(And(O >= 0, O <= 9))
    s.add(And(R >= 0, R <= 9))
    s.add(And(S >= 0, S <= 9))
    s.add(And(T >= 0, T <= 9))
    s.add(And(V >= 0, V <= 9))
    VIOLIN, VIOLA, SONATA, TRIO = Ints('VIOLIN VIOLA SONATA TRIO')
    s.add(VIOLIN == 100000 * V + 10000 * I + 1000 * O + 100 * L + 10 * I + N)
    s.add(VIOLA == 10000 * V + 1000 * I + 100 * O + 10 * L + A)
    s.add(SONATA == 100000 * S + 10000 * O + 1000 * N + 100 * A + 10 * T + A)
    s.add(TRIO == 1000 * T + 100 * R + 10 * I + O)
    s.add(VIOLIN + VIOLIN + VIOLA == TRIO + SONATA)
    # solution
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)
        print(m[VIOLIN].as_long() + m[VIOLIN].as_long() + m[VIOLA].as_long())
        print(m[TRIO].as_long()+m[SONATA].as_long())


def alphametics_2():
    C, O, N, T, E, D, I, M, A, R, S, L, U = Ints('C O N T E D I M A R S L U')
    s = Solver()
    s.add(Distinct(C, O, N, T, E, D, I, M, A, R, S, L, U))
    s.add(And(C >= 0, C <= 9))
    s.add(And(O >= 0, O <= 9))
    s.add(And(N >= 0, N <= 9))
    s.add(And(T >= 0, T <= 9))
    s.add(And(E >= 0, E <= 9))
    s.add(And(D >= 0, D <= 9))
    s.add(And(I >= 0, I <= 9))
    s.add(And(M >= 0, M <= 9))
    s.add(And(A >= 0, A <= 9))
    s.add(And(R >= 0, R <= 9))
    s.add(And(S >= 0, S <= 9))
    s.add(And(L >= 0, L <= 9))
    s.add(And(U >= 0, U <= 9))
    CONTE, DIMAIO, TRIDICO, MERDA, DI, CULO = Ints('CONTE DIMAIO TRIDICO MERDA DI CULO')
    s.add(CONTE == 10000 * C + 1000 * O + 100 * N + 10 * T + 1 * E)
    s.add(DIMAIO == 100000 * D + 10000 * I + 1000 * M + 100 * A + 10 * I + 1 * O)
    s.add(TRIDICO == 1000000 * T + 100000 * R + 10000 * I + 1000 * D + 100 * I + 10 * C + 1 * O)
    s.add(MERDA == 10000 * M + 1000 * E + 100 * R + 10 * D + 1 * A)
    s.add(DI == 10 * D + 1 * I)
    s.add(CULO == 1000 * C + 100 * U + 10 * L + 1 * O)
    s.add(CONTE + DIMAIO + TRIDICO == MERDA + DI + CULO)
    # solution
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)
        print(m[CONTE].as_long() + m[DIMAIO].as_long() + m[TRIDICO].as_long())
        print(m[MERDA].as_long()+m[DI].as_long()+m[CULO].as_long())


if __name__ == '__main__':
    # hanoi()
    alphametics_2()
