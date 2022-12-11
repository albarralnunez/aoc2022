from pathlib import Path
from src.python.day10.day10 import problem_1, Noop, AddX, generate_cycles, State


def test_problem_1():
    input_path = Path("files/day10/test_input.txt")
    assert problem_1(input_path) == 13140


def test_problem_1_2():
    instructions = iter(
        [
            Noop(),
            AddX(3),
            AddX(-5),
        ]
    )

    cycles = list(generate_cycles(instructions))
    assert cycles[-1] == State(instruction=AddX(-5), register_x=4, cycle_number=5)
