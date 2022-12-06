from pathlib import Path
from typing import Iterable
from itertools import takewhile


def read_input(input_path: Path) -> str:
    with input_path.open() as f:
        return f.read().strip()


def chunk_in_slices(input: str, chunk_size: int) -> Iterable[str]:
    for index in range(len(input)):
        yield input[index : index + chunk_size]


def is_all_diferent(input: str) -> bool:
    return len(set(input)) == len(input)


def solver(input: str, marker_size) -> int:
    sliced_input = chunk_in_slices(input, marker_size)
    result = takewhile(lambda x: x is False, map(is_all_diferent, sliced_input))
    return len(list(result)) + marker_size


def main():
    input_path = Path("files/day6/input.txt")
    input = read_input(input_path)
    solution = solver(input, 4)
    print(f"Problem 1: {solution}")
    input = read_input(input_path)
    solution = solver(input, 14)
    print(f"Problem 2: {solution}")


if __name__ == "__main__":
    main()
