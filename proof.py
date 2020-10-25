#
# https://stackoverflow.com/questions/29577754/getting-proof-from-z3py#29585088
#
# 24.10.2020
#

from z3 import *


if __name__ == '__main__':
    set_param('parallel.enable', True)
    set_param(proof=True)
    #
    x = Int('x')
    s = Solver()
    s.add(x*x == x + 1)
    s.add(1/x == x - 1)
    # solution
    r = s.check()
    print(r)
    m = s.model()
    print(m)
    p = s.proof()
    print(p)
