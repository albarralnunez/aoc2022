from typing import IO
from pathlib import Path

def cast_to_ints(row: str) -> list:
    return list(map(int, row))

def read_file(f: IO) -> list:
    return list(map(
        cast_to_ints,
        map(lambda x: x.strip(), f.readlines()
    )))

def is_visible_edge_x(
    matrix: list[list[int]],
    x: int, y: int
) -> bool:
    i = 0
    value = matrix[x][y]
    while x-i >= 0:
        if matrix[x-i][y] >= value:
            value = matrix[x-i][y]
        else:
            return False
        i += 1
    i = 0
    value = matrix[x][y]
    while x+i <= len(matrix) - 1:
        if matrix[x+i][y] >= value:
            value = matrix[x+i][y]
        else:
            return False
        i += 1
    return True

def is_visible_edge_y(
    matrix: list[list[int]],
    x: int, y: int
) -> bool:
    i = 0
    value = matrix[x][y]
    while y-i > 0:
        if matrix[x][y-i] >= value:
            value = matrix[x][y-i]
        else:
            return False
        i += 1
    i = 0
    value = matrix[x][y]
    while y+i < len(matrix[0]) - 1:
        if matrix[x][y+i] >= value:
            value = matrix[x][y+i]
        else:
            return False
        i += 1
    return True

def is_visible(matrix: list[list[int]], x: int, y: int) -> bool:
    if (
        is_visible_edge_x(matrix, x, y) 
        and is_visible_edge_y(matrix, x, y)
    ):
        return True
    return False

def problem_1(input_path: Path):
    visible = 0
    with input_path.open() as f:
        problem_matrix = read_file(f)
    for y, col in enumerate(problem_matrix):
        for x, _ in enumerate(col):
            if is_visible(problem_matrix, x, y):
                visible += 1
    return visible

def main():
    input_path = Path("files/day8/test_input.txt")
    solution = problem_1(input_path)
    print("Problem 1:")
    print(solution)


if __name__ == "__main__":
    main()
