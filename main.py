# 23.9.2020

from z3 import *


def main(name):
    A = IntSort()
    B = BoolSort()
    R = Function('R', A, A, B)
    TC_R = TransitiveClosure(R)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

