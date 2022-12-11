from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterator
import math
from os import system, name
from time import sleep
import copy
from termcolor import colored, cprint


def highlight(text: str, color: str = "white", on_color: str = "on_blue"):
    return colored(text, "white", "on_blue")


def highlight_cursor(text: str, color: str = "white", on_color: str = "on_red"):
    return colored(text, "white", "on_red")


def clear():
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux
    else:
        _ = system("clear")


@dataclass
class Instruction:
    @classmethod
    def from_str(cls, line: str) -> "Instruction":
        if line.startswith("noop"):
            return Noop()
        elif line.startswith("addx"):
            _, value = line.split(" ")
            return AddX(value=int(value))
        else:
            raise ValueError(f"Unknown instruction: {line}")


@dataclass
class AddX(Instruction):
    value: int


@dataclass
class Noop(Instruction):
    ...


def initial_state_visualization() -> list[list[str]]:
    return [["." for _ in range(40)] for _ in range(6)]


@dataclass
class State:
    instruction: Instruction
    register_x: int
    cycle_number: int
    visualization: list[list[str]] = field(
        default_factory=initial_state_visualization, repr=False, compare=False
    )

    @property
    def pointer(self) -> int:
        return self.cycle_number - 1

    def position_to_x_y(self, position: int) -> tuple[int, int]:
        x = position % 40
        y = math.floor(position / 40)
        return x, y

    def __post_init__(self):
        if self.has_to_print():
            position = self.position_to_x_y(self.pointer)
            self.visualization[position[1]][position[0]] = "#"

    def has_to_print(self) -> bool:
        row = self.position_to_x_y(self.pointer)[1]
        slice_pointer = self.register_x + row * 40
        if self.pointer in [slice_pointer, slice_pointer + 1, slice_pointer - 1]:
            return True
        return False

    def print(self, debug: bool = False) -> str:
        matrix = copy.deepcopy(self.visualization)
        if debug is True:
            pointer = self.position_to_x_y(self.pointer)
            matrix[pointer[1]][pointer[0]] = highlight_cursor(matrix[pointer[1]][pointer[0]])
            row = self.position_to_x_y(self.pointer)[1]
            slice_pointer = self.register_x + row * 40
            sprint_0 = self.position_to_x_y(slice_pointer - 1)
            sprit_1 = self.position_to_x_y(slice_pointer)
            spirit_2 = self.position_to_x_y(slice_pointer + 1)
            matrix[sprint_0[1]][sprint_0[0]] = highlight(matrix[sprint_0[1]][sprint_0[0]])
            if sprit_1[0] <= 39 and sprit_1[1] <= 5:
                matrix[sprit_1[1]][sprit_1[0]] = highlight(matrix[sprit_1[1]][sprit_1[0]])
            if spirit_2[0] <= 39 and spirit_2[1] <= 5:
                matrix[spirit_2[1]][spirit_2[0]] = highlight(matrix[spirit_2[1]][spirit_2[0]])
        repr = "\n".join(["".join(i) for i in matrix])
        return repr

    @property
    def signal_strength(self) -> int:
        return self.register_x * self.cycle_number

    def repr(self):
        return "\n".join(["".join(row) for row in self.visualization])


def generate_cycles(instructions: Iterator[Instruction]) -> Iterator[State]:
    cycle_number = 1
    register_x = 1
    s = State(
        instruction=Noop(),
        cycle_number=cycle_number,
        register_x=register_x,
    )
    for instruction in instructions:
        if isinstance(instruction, AddX):
            s = State(
                instruction=instruction,
                cycle_number=cycle_number,
                register_x=register_x,
                visualization=s.visualization,
            )
            yield s
            cycle_number += 1
            s = State(
                instruction=instruction,
                cycle_number=cycle_number,
                register_x=register_x,
                visualization=s.visualization,
            )
            yield s
            register_x += instruction.value
            cycle_number += 1
        elif isinstance(instruction, Noop):
            s = State(
                instruction=instruction,
                cycle_number=cycle_number,
                register_x=register_x,
                visualization=s.visualization,
            )
            yield s
            cycle_number += 1


def problem_1(input_path: Path) -> int:
    signal_strength = 0
    with open(input_path) as f:
        instructions = map(Instruction.from_str, f)
        cycles = generate_cycles(instructions)
        print()
        for c in cycles:
            if (c.cycle_number - 20) % 40 == 0 or c.cycle_number == 20:
                signal_strength += c.signal_strength
    return signal_strength


def problem_2(input_path: Path) -> Iterator[State]:
    signal_strength = 0
    with open(input_path) as f:
        instructions = map(Instruction.from_str, f)
        cycles = generate_cycles(instructions)
        for c in cycles:
            yield c
    return signal_strength


def print_day_10(input_path: Path):
    p1 = problem_1(input_path)
    p2 = problem_2(input_path)
    for c in p2:
        clear()
        print("*" * 40)
        print(f"Problem 1: {p1}")
        print("Problem 2:")
        print(c.print(debug=True))
        print("*" * 40)
        sleep(0.1)


def main():
    # input_path = Path("files/day10/test_input.txt")
    input_path = Path("files/day10/input.txt")
    print_day_10(input_path)


if __name__ == "__main__":
    main()
