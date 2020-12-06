#
#
# 6.12.2020
#
#

from time import perf_counter
import matplotlib

matplotlib.use('GTK3Cairo')
from graph_tool import Graph
from graph_tool.draw import graph_draw
from pkg.heuristics import uniform_cost
from pkg.colors import color
from pkg.search import ida_star_search

HEURISTIC = uniform_cost
TRANSITION_COST = 1


def alphametics_star():
    g = Graph()
    v1 = g.add_vertex()
    v2 = g.add_vertex()
    e = g.add_edge(v1, v2)
    # graph_draw(g, vertex_text=g.vertex_index)

    print(color('yellow', 'start search'))
    puzzle = []
    solved = []
    size = 1
    t_start = perf_counter()
    res = ida_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST)
    t_delta = perf_counter() - t_start
    print(color('yellow', 'search duration:') + ' %.4f second(s)' % t_delta)


if __name__ == '__main__':
    alphametics_star()
