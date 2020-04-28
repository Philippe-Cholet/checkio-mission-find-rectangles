from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee

from tests import TESTS

from itertools import product


# Don't want to update the checker only to add `return False, args` 10 times.
def manage_asserts(func):
    def wrapper(*args):
        try:
            func(*args)
        except AssertionError as error:
            return False, error.args[0]
        return True, 'Great!'
    return wrapper


@manage_asserts
def checker(grid, result):
    # Result is a list or is not iterable after JSON treated it.
    assert isinstance(result, list), ('Your result must be iterable.', [])
    nb_rows, nb_cols = len(grid), len(grid[0])
    colored_grid = [[0 for _ in range(nb_cols)] for _ in range(nb_rows)]
    prev_rects = set()
    for color, rect in enumerate(result, 1):
        assert (isinstance(rect, (tuple, list)) and len(rect) == 4
                and all(isinstance(coord, int) for coord in rect)), \
            (f'{rect} does not represent a rectangle, '
             'it should be a tuple/list of four integers.',
             list(prev_rects))
        assert tuple(rect) not in prev_rects, \
            (f'You gave the same rectangle {rect} twice.',
             list(prev_rects))
        x1, y1, x2, y2 = rect
        assert x1 <= x2 and y1 <= y2, \
            (f'The rectangle {rect} must be '
             '(top left coords, bottom right coords).',
             list(prev_rects))
        prev_rects.add(tuple(rect))
        for x, y in ((x1, y1), (x2, y2)):
            assert 0 <= x < nb_rows and 0 <= y < nb_cols, \
                (f'The rectangle {rect} contains {x, y} '
                 'which is not in the grid.',
                 list(prev_rects))
        area = (x2 + 1 - x1) * (y2 + 1 - y1)
        grid_area = None
        for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
            assert not colored_grid[x][y], \
                (f'Rectangle #{color} intersects '
                 f'rectangle #{colored_grid[x][y]} at {x, y}.',
                 list(prev_rects))
            colored_grid[x][y] = color
            if grid[x][y]:
                assert grid_area is None, \
                    (f'The rectangle {rect} contains two area values: '
                     f'{grid_area} and {grid[x][y]}.',
                     list(prev_rects))
                grid_area = grid[x][y]
                assert grid[x][y] == area, \
                    (f'The rectangle {rect} have area={area} '
                     f'and contains another area value: {grid[x][y]}.',
                     list(prev_rects))
        assert grid_area is not None, (f'{rect} contains no area value.',
                                       list(prev_rects))

    nb_uncovered = sum(not cell for row in colored_grid for cell in row)
    assert not nb_uncovered, (f'{nb_uncovered} cells are still not covered.',
                              list(prev_rects))


dumb_cover_just_to_accept_sets = '''
def cover(func, in_data):
    return list(func(in_data))
'''


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        checker=checker,
        function_name={
            'python': 'rectangles',
            # 'js': 'rectangles',
        },
        cover_code={
            'python-3': dumb_cover_just_to_accept_sets,
            # 'js-node': ...,
        },
    ).on_ready,
)
