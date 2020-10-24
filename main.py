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


move_names = ["MOVE 1 -> 2", "MOVE 2 -> 1",
              "MOVE 1 -> 3", "MOVE 3 -> 1",
              "MOVE 2 -> 3", "MOVE 3 -> 2"]


def move(state, op):
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
            L |= 2 ** i
        if i in stack[1]:
            C |= 2 ** i
        if i in stack[2]:
            R |= 2 ** i
    #
    # solution
    # r = s.check()
    # print(r)
    # if r == sat:
    #    m = s.model()
    #    print(m)


def alphametics():
    # VIOLIN + VIOLIN + VIOLA = TRIO + SONATA
    A, I, L, N, O, R, S, T, V = Ints('A, I, L, N, O, R, S, T, V')
    s = Solver()
    s.add(Distinct(A, I, L, N, O, R, S, T, V))
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
        print(m[TRIO].as_long() + m[SONATA].as_long())


def char_to_idx(c):
    return ord(c) - ord('A')


def idx_to_char(i):
    return chr(ord('A') + i)


# construct expression in form like:
# 10000000*L+1000000*U+100000*N+10000*C+1000*H+100*E+10*O+N
def list_to_expr(lst):
    coeff = 1
    _sum = 0
    for var in lst[::-1]:
        _sum = _sum + var * coeff
        coeff = coeff * 10
    return _sum


def alphametics_gen():
    # this table has 10 items, it reflects character for each number:
    digits = [Int('digit_%d' % i) for i in range(10)]

    # this is "reverse" table, it has value for each letter:
    letters = [Int('letter_%d' % i) for i in range(26)]

    s = Solver()

    # all items in digits[] table must be distinct, because no two letters can share same number:
    s.add(Distinct(digits))

    # all numbers are in 0..25 range, because each number in this table defines character:
    for i in range(10):
        s.add(And(digits[i] >= 0, digits[i] < 26))

    # define "reverse" table.
    # letters[i] is 0..9, depending on which digits[] item contains this letter:
    for i in range(26):
        s.add(letters[i] ==
              If(digits[0] == i, 0,
                 If(digits[1] == i, 1,
                    If(digits[2] == i, 2,
                       If(digits[3] == i, 3,
                          If(digits[4] == i, 4,
                             If(digits[5] == i, 5,
                                If(digits[6] == i, 6,
                                   If(digits[7] == i, 7,
                                      If(digits[8] == i, 8,
                                         If(digits[9] == i, 9, 99999999)))))))))))

    # the last word is "sum" all the rest are "addends":

    words = ['MERLO', 'PIPPA', 'VENDUTO', 'CIPPA', 'BACATO', 'PUPAZZO', 'PAGLIACCIO', 'BUFFONE', 'PINOCCHIO', 'FETENTE', 'PICIU', 'MONA',
             'CIUMMELLO', 'DRACULA', 'CORNUTO', 'ASSASSINO', 'PREZZOLATO', 'BARACCONE', 'PORCO', 'CUCCO', 'CANAGLIA', 'SEDANO', 'CARCIOFO',
             'ZOZZONE', 'PIRLA', 'ZOCCOLA', 'ZIMBELLO', 'MERDACCIA', 'FINOCCHIO', 'BAVOSO', 'TRADITORE', 'INDEGNO',
             'ALLUPATO', 'DROGATO', 'DELUCA']

    words_total = len(words)

    word = [Int('word_%d' % i) for i in range(words_total)]
    word_used = [Bool('word_used_%d' % i) for i in range(words_total)]

    # last word is always used:
    s.add(word_used[words_total - 1] == True)

    # s.add(word_used[words.index('CAKE')])
    # s.add(word_used[words.index('ZINGARETTI')])

    for i in range(words_total):
        # get list of letters for the word:
        lst = [letters[char_to_idx(c)] for c in words[i]]
        # construct expression for letters. it must be equal to the value of the word:
        s.add(word[i] == list_to_expr(lst))
        # if word_used, word's value must be less than 99999999, i.e., all letters are used in the word:
        s.add(If(word_used[i], word[i], 0) < 99999999)

    # if word_used, add value of word to the whole expression
    expr = [If(word_used[i], word[i], 0) for i in range(words_total - 1)]
    # sum up all items in expression. sum must be equal to the value of the last word:
    s.add(sum(expr) == word[-1])

    # solution
    r = s.check()
    print(r)
    if r == sat:
        m = s.model()
        print(m)
        for i in range(words_total):
            # if word_used, print it:
            if str(m[word_used[i]]) == "True" or i + 1 == words_total:
                print(words[i])

        for i in range(26):
            # it letter is used, print it:
            if m[letters[i]].as_long() != 99999999:
                print(idx_to_char(i), m[letters[i]])


if __name__ == '__main__':
    set_param('parallel.enable', True)
    # set_param(proof=True)
    # hanoi()
    alphametics_gen()
