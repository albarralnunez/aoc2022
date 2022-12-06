from typing import Iterator, ClassVar, IO
import dataclasses
from pathlib import Path
import re


@dataclasses.dataclass
class Stack:
    cargo: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Instruction:
    move: int
    move_from: int
    move_to: int


@dataclasses.dataclass
class Ship:
    stacks: list[Stack] = dataclasses.field(default_factory=list)

    def add_to_stack(self, position: int, element: str) -> None:
        self.stacks[position].cargo = [element] + self.stacks[position].cargo
    
    def _split(self, slice: list, index: int) -> tuple[list, list]:
        return slice[:len(slice)-index], slice[len(slice)-index:]

    def move_p1(self, instruction: Instruction) -> None:
        new_stack, items_to_move = self._split(self.stacks[instruction.move_from-1].cargo, instruction.move)
        self.stacks[instruction.move_from-1].cargo = new_stack
        self.stacks[instruction.move_to-1].cargo += items_to_move[::-1]

    def move_p2(self, instruction: Instruction) -> None:
        new_stack, items_to_move = self._split(self.stacks[instruction.move_from-1].cargo, instruction.move)
        self.stacks[instruction.move_from-1].cargo = new_stack
        self.stacks[instruction.move_to-1].cargo += items_to_move

    def result(self) -> str:
        return "".join(map(lambda x: x.cargo[-1], self.stacks))
    
    def __str__(self) -> str:
        return "\n".join([str("".join(stack.cargo)) for stack in self.stacks])


@dataclasses.dataclass
class ShipFactory:
    blueprint_line_re: ClassVar[re.Pattern] = re.compile(r"(\[\w\]\s?|\s{4})")

    instruction_line_re: ClassVar[re.Pattern] = re.compile("move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)")

    def _blueprint_to_ship(self, lines: list[str], ship: Ship) -> Ship:
        size = int(lines.pop()[-3])
        for i in range(size):
            ship.stacks.append(Stack())
        for line in lines:
            line_match = self.blueprint_line_re.findall(line)
            for i, element in enumerate(line_match):
                if element.startswith("["):
                    ship.add_to_stack(i, element[1])
        return ship

    def _read_blueprint(self, f) -> Iterator[Instruction]:
        blueprint = []
        for line in f:
            if line == "\n":
                break
            blueprint.append(line)
        return blueprint
    
    def _read_instructions(self, f: IO) -> Iterator[Instruction]: 
        for line in f:
            match = self.instruction_line_re.match(line) 
            yield Instruction(
                move=int(match.group(1)),
                move_from=int(match.group(2)),
                move_to=int(match.group(3))
            )

    def read_input(self, f: IO) -> tuple[Ship, list[Instruction]]:
        ship = Ship()
        blueprint = self._read_blueprint(f)
        self._blueprint_to_ship(blueprint, ship)
        instructions = self._read_instructions(f) 
        return ship, instructions
    
    def read(self, f: IO) -> tuple[Ship, list[Instruction]]:
        ship = Ship()
        blueprint = self._read_blueprint(f)
        self._blueprint_to_ship(blueprint, ship)
        instructions = self._read_instructions(f) 
        return ship, instructions

def problem1(f: IO) -> int:
    reader = ShipFactory()
    ship, instructions = reader.read_input(f)
    for instruction in instructions:
        ship.move_p1(instruction)
    return ship

def problem2(f: IO) -> int:
    reader = ShipFactory()
    ship, instructions = reader.read_input(f)
    for instruction in instructions:
        ship.move_p2(instruction)
    return ship

def main():
    # input_path = Path("files/day5/test_input.txt")
    input_path = Path("files/day5/input.txt")
    with input_path.open() as f:
        solution = problem1(f)
        print("Problem 1:")
        print(solution.result())
        print()
    with input_path.open() as f:
        solution = problem2(f)
        print("Problem 2:")
        print(solution.result())


if __name__ == "__main__":
    main()
