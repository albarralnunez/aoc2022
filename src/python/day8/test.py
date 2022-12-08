import pytest
from day8 import is_visible_edge_x


@pytest.mark.parametrize(
    "x, y, expected",
    (
        (2, 2, False),
        # (0, 0, True),
        # (0, 4, True),
        # (4, 0, True),
        # (3, 1, True),
        # (3, 1, True),
    )
)
def test_is_visible_edge_x(x, y, expected):
    matrix = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9],
    ]
    assert (
        is_visible_edge_x(matrix, x, y) == expected,
        f"Failed for {x}, {y}"
    )