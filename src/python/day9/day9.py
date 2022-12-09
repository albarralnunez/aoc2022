from typing import Iterator
from pathlib import Path
from dataclasses import dataclass, field, InitVar
from enum import Enum
import math


class Direction(Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def first_position(cls) -> "Point":
        return cls(0, 0)

    def move(self, vector: tuple[int, int]) -> "Point":
        return Point(self.x + vector[0], self.y + vector[1])


@dataclass
class Move:
    direction: Direction
    distance: int

    @classmethod
    def from_tuple(cls, direction: str, distance: int) -> "Move":
        return cls(Direction(direction), distance)


@dataclass
class Rope:
    knots: list[Point] = field(default_factory=list)
    tail_visited: list[Point] = field(default_factory=list)
    knots_number: InitVar[int] = 2

    def __post_init__(self, knots_number: int):
        self.knots = [Point.first_position() for _ in range(knots_number)]

    def visited_repr(self, x_size: int = 10, y_size: int = 10) -> str:
        board_line = ["."] * x_size
        board = [board_line.copy() for _ in range(y_size)]
        for point in self.tail_visited:
            board[point.y][point.x] = "#"
        return "\n".join(["".join(x) for x in board[::-1]])

    def repr(self, x_size: int = 10, y_size: int = 10, offset: int = 0) -> str:
        board_line = ["."] * x_size
        board = [board_line.copy() for _ in range(y_size)]
        board[offset][offset] = "s"
        for i, knot in enumerate(self.knots):
            if board[knot.y + offset][knot.x + offset] in [".", "s"]:
                board[knot.y + offset][knot.x + offset] = str(i)
        return "\n".join(["".join(x) for x in board[::-1]])

    def move_knot(self, i: int, direction: Direction):
        if direction == Direction.RIGHT:
            self.knots[i] = Point(self.knots[i].x + 1, self.knots[i].y)
        if direction == Direction.LEFT:
            self.knots[i] = Point(self.knots[i].x - 1, self.knots[i].y)
        if direction == Direction.UP:
            self.knots[i] = Point(self.knots[i].x, self.knots[i].y + 1)
        if direction == Direction.DOWN:
            self.knots[i] = Point(self.knots[i].x, self.knots[i].y - 1)

    def _get_vector_lenght(self, vector: tuple[int, int]) -> int:
        return (vector[0] ** 2 + vector[1] ** 2) ** 0.5

    def _get_vector(self, head: Point, tail: Point) -> tuple[int, int]:
        return (head.x - tail.x, head.y - tail.y)

    def follow(self, i: int):
        vector = self._get_vector(self.knots[i], self.knots[i + 1])
        vector_lenght = self._get_vector_lenght(vector)
        if vector_lenght < 2:
            return
        if vector[0] > 0:
            new_x = math.ceil(vector[0] / 2)
        else:
            new_x = math.floor(vector[0] / 2)
        if vector[1] > 0:
            new_y = math.ceil(vector[1] / 2)
        else:
            new_y = math.floor(vector[1] / 2)
        self.knots[i + 1] = self.knots[i + 1].move((new_x, new_y))
        if i + 1 == len(self.knots) - 1:
            self.tail_visited.append(self.knots[len(self.knots) - 1])

    def move(self, move: Move, debug: bool = False, size: int = 6, offset: int = 0):
        for _ in range(move.distance):
            self.move_knot(0, move.direction)
            for i in range(len(self.knots) - 1):
                self.follow(i)
        if debug is True:
            print("#" * size)
            print(self.repr(size, size, offset=offset))
            input()

    def run(
        self, moves: Iterator[Move], debug: bool = False, size: int = 6, offset: int = 0
    ):
        for move in moves:
            self.move(move, debug=debug, size=size, offset=offset)


def moves_builder(input_path: Path) -> Iterator[Move]:
    with open(input_path) as f:
        return map(
            lambda x: Move.from_tuple(x[0], int(x[1])),
            map(lambda x: x.split(" "), map(lambda x: x.strip(), f.readlines())),
        )


def problem_1(input_path: Path):
    moves = moves_builder(input_path)
    rope = Rope()
    rope.run(moves, debug=False)
    return len(set(rope.tail_visited)) + 1


def problem_2(input_path: Path, n: int):
    moves = moves_builder(input_path)
    rope = Rope(knots_number=n)
    # rope.run(moves, debug=True, size=30, offset=15)
    rope.run(moves, debug=False)
    return len(set(rope.tail_visited)) + 1


def main():
    # input_path = Path("files/day9/test_input.txt")
    input_path = Path("files/day9/input.txt")
    print(f"Problem 1: {problem_1(input_path)}")
    # input_path = Path("files/day9/test_input_2.txt")
    input_path = Path("files/day9/input.txt")
    print(f"Problem 2: {problem_2(input_path, 10)}")


if __name__ == "__main__":
    main()
