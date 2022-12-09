import pytest
from day8 import is_visible, problem_2


@pytest.mark.parametrize(
    "x, y, expected",
    (
        (0, 1, True),
        (1, 1, True),
        (1, 3, False),
        (2, 1, True),
        (2, 2, False),
        (1, 2, True),
        (1, 4, True),
        (3, 4, True),
    ),
)
def test_is_visible(x, y, expected):
    matrix_raw = ["30373", "25912", "65332", "33549", "35390"]
    matrix: list[list[int]] = [list(map(int, row)) for row in matrix_raw]
    assert (
        is_visible(matrix, x, y) == expected
    ), f"Failed for {x}, {y}, value {matrix[x][y]}"


def test_problem_2():
    matrix_raw = ["30373", "25912", "65332", "33549", "35390"]
    matrix: list[list[int]] = [list(map(int, row)) for row in matrix_raw]
    assert problem_2(matrix) == 12
