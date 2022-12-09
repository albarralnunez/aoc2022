from typing import IO
from pathlib import Path


def cast_to_ints(row: str) -> list:
    return list(map(int, row))


def read_file(f: IO) -> list:
    return list(map(cast_to_ints, map(lambda x: x.strip(), f.readlines())))


def is_in_the_edge(matrix: list[list[int]], x: int, y: int) -> bool:
    return x == 0 or y == 0 or x == len(matrix) - 1 or y == len(matrix[0]) - 1


def is_visible_edge_x_front(matrix: list[list[int]], x: int, y: int) -> bool:
    i = 1
    while x - i >= 0:
        if matrix[x][y] <= matrix[x - i][y]:
            return False
        i += 1
    return True


def is_visible_edge_x_back(matrix: list[list[int]], x: int, y: int) -> bool:
    i = 1
    while x + i < len(matrix):
        if matrix[x][y] <= matrix[x + i][y]:
            return False
        i += 1
    return True


def is_visible_edge_y_back(matrix: list[list[int]], x: int, y: int) -> bool:
    i = 1
    while y - i >= 0:
        if matrix[x][y] <= matrix[x][y - i]:
            return False
        i += 1
    return True


def is_visible_edge_y_front(matrix: list[list[int]], x: int, y: int) -> bool:
    i = 1
    while y + i < len(matrix[0]):
        if matrix[x][y] <= matrix[x][y + i]:
            return False
        i += 1
    return True


def get_score_x_back(matrix: list[list[int]], x: int, y: int) -> int:
    i = 1
    while x - i > 0:
        if matrix[x][y] <= matrix[x - i][y]:
            break
        i += 1
    return i


def get_score_x_forward(matrix: list[list[int]], x: int, y: int) -> int:
    i = 1
    while x + i < len(matrix) - 1:
        if matrix[x][y] <= matrix[x + i][y]:
            break
        i += 1
    return i


def get_score_y_back(matrix: list[list[int]], x: int, y: int) -> int:
    i = 1
    while y - i > 0:
        if matrix[x][y] <= matrix[x][y - i]:
            break
        i += 1
    return i


def get_score_y_forward(matrix: list[list[int]], x: int, y: int) -> int:
    i = 1
    while y + i < len(matrix[0]) - 1:
        if matrix[x][y] <= matrix[x][y + i]:
            break
        i += 1
    return i


def is_visible(matrix: list[list[int]], x: int, y: int) -> bool:
    if is_in_the_edge(matrix, x, y):
        return True
    result = (
        is_visible_edge_x_front(matrix, x, y)
        or is_visible_edge_x_back(matrix, x, y)
        or is_visible_edge_y_front(matrix, x, y)
        or is_visible_edge_y_back(matrix, x, y)
    )
    return result


def problem_1(problem_matrix: list[list[int]]):
    visible = 0
    for x, raw in enumerate(problem_matrix):
        for y, _ in enumerate(raw):
            if is_visible(problem_matrix, x, y):
                visible += 1
    return visible


def get_score(matrix: list[list[int]], x: int, y: int) -> int:
    score_x_back = get_score_x_back(matrix, x, y)
    score_x_forward = get_score_x_forward(matrix, x, y)
    score_y_back = get_score_y_back(matrix, x, y)
    score_y_forward = get_score_y_forward(matrix, x, y)
    result = score_x_back * score_x_forward * score_y_back * score_y_forward
    return result


def problem_2(problem_matrix: list[list[int]]):
    max_score = 0
    for x, raw in enumerate(problem_matrix):
        for y, _ in enumerate(raw):
            if is_in_the_edge(problem_matrix, x, y):
                continue
            score = get_score(problem_matrix, x, y)
            max_score = max(max_score, score)
    return max_score


def main():
    # input_path = Path("files/day8/test_input.txt")
    input_path = Path("files/day8/input.txt")
    with input_path.open() as f:
        problem_matrix = read_file(f)
    print("Problem 1: ", problem_1(problem_matrix))
    print("Problem 2: ", problem_2(problem_matrix))


if __name__ == "__main__":
    main()
