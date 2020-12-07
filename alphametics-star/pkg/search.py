from itertools import count
from heapq import heappush, heappop
from collections import deque
from math import inf

# puzzle definition
# VIOLIN + VIOLIN + VIOLA = TRIO + SONATA
letter_model = {'A': 0, 'I': 0, 'L': 0, 'N': 0, 'O': 0, 'R': 0, 'S': 0, 'T': 0, 'V': 0}


def next_assigment(letter_model):
    # for c in it.permutations([0,1,2], 3):
    # for k in letter_model:
    pass


def clone_and_swap(data, y0, y1):
    clone = list(data)
    tmp = clone[y0]
    clone[y0] = clone[y1]
    clone[y1] = tmp
    return tuple(clone)


def possible_moves(data, size):
    res = []
    y = data.index(EMPTY_TILE)
    if y % size > 0:
        left = clone_and_swap(data, y, y - 1)
        res.append(left)
    if y % size + 1 < size:
        right = clone_and_swap(data, y, y + 1)
        res.append(right)
    if y - size >= 0:
        up = clone_and_swap(data, y, y - size)
        res.append(up)
    if y + size < len(data):
        down = clone_and_swap(data, y, y + size)
        res.append(down)
    return res


def ida_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST):
    def search(path, g, bound, evaluated):
        evaluated += 1
        node = path[0]
        f = g + HEURISTIC(node, solved, size)
        if f > bound:
            return f, evaluated
        if node == solved:
            return True, evaluated
        ret = inf
        moves = possible_moves(node, size)
        for m in moves:
            if m not in path:
                path.appendleft(m)
                t, evaluated = search(path, g + TRANSITION_COST, bound, evaluated)
                if t is True:
                    return True, evaluated
                if t < ret:
                    ret = t
                path.popleft()
        return ret, evaluated

    bound = HEURISTIC(puzzle, solved, size)
    path = deque([puzzle])
    evaluated = 0
    while path:
        t, evaluated = search(path, 0, bound, evaluated)
        if t is True:
            path.reverse()
            return (True, path, {'space': len(path), 'time': evaluated})
        elif t is inf:
            return (False, [], {'space': len(path), 'time': evaluated})
        else:
            bound = t
