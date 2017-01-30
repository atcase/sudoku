from itertools import chain, filterfalse
from operator import itemgetter


def print_sudoku(s):
    """ Display a sudoku `s` stored as a flat list of cells, with each cell either [] (unsolved) or [n] (solved) """
    for row in range(9):
        print(*[c[0] if c else '.' for c in s[row * 9:row * 9 + 9]], sep=' ')
    print()


def copy_sudoku(s):
    return [c[:] for c in s[:]]


def same_row_as(idx):
    """ Return indexes to cells in the same row as `idx` """
    base = idx // 9 * 9
    return range(base, base + 9)


def same_col_as(idx):
    """ Return indexes to cells in the same column as `idx` """
    return range(idx % 9, 81, 9)


def same_box_as(idx):
    """ Return indexes to cells in the same 'box' as `idx` """
    base = idx // 27 * 27 + idx // 3 % 3 * 3
    return chain(range(base, base + 3), range(base + 9, base + 12), range(base + 18, base + 21))


def get_possibilities(s, idx):
    """ Return a set of all the possible solutions to the cell at location `idx` """
    possibilities = set(range(1, 10))
    possibilities -= set(s[i][0] for i in chain(same_row_as(idx), same_col_as(idx), same_box_as(idx)) if s[i])
    return possibilities


def iter_unsolved(s):
    return filterfalse(itemgetter(1), enumerate(s))


def reduce_sudoku_and_check_solvability(s):
    """ Solve any cells of `s` in-place where only a single value is possible, returning False if `s` is unsolvable """
    repeat = False
    for idx, cell in iter_unsolved(s):
        possibilities = get_possibilities(s, idx)
        if len(possibilities) == 1:
            cell.append(possibilities.pop())
            repeat = True
        elif len(possibilities) == 0:
            return False  # Impossible!
    if repeat:
        return reduce_sudoku_and_check_solvability(s)
    return True


def solve(s):
    """ Returns the solution to the sudoku `s` if it exists, otherwise returns False """
    if not reduce_sudoku_and_check_solvability(s):
        return False
    try:
        first_unsolved_idx = s.index([])
    except ValueError:
        return s  # It's already solved!

    for solution in get_possibilities(s, first_unsolved_idx):
        s2 = copy_sudoku(s)
        s2[first_unsolved_idx] = [solution]
        s2 = solve(s2)
        if s2:
            return s2
    return False  # Couldn't solve it


s = [[] for _ in range(81)]  # empty sudoku
print_sudoku(s)
solved_sudoku = solve(s)
if solved_sudoku:
    print_sudoku(solved_sudoku)
else:
    print("Couldn't solve it")
