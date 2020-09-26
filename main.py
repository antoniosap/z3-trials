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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tr()
