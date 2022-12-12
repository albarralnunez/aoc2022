from termcolor import colored
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, IO, ClassVar, Pattern, Iterator, Optional
import re
import operator
from functools import partial
import math


@dataclass
class Item:
    worry_level: int

    def operation(self, operation: Callable) -> "Item":
        self.worry_level = operation(self.worry_level)
        return self

    def shrink(self, divide: bool = False, module: Optional[int] = None) -> "Item":
        if divide is True:
            self.worry_level //= 3
        elif module is not None:
            self.worry_level %= module
        else:
            raise ValueError("Invalid arguments")
        return self


@dataclass
class MonkeyTest:
    test_number: int
    true: int
    false: int

    def test(self, number: int) -> bool:
        return number % self.test_number == 0


@dataclass
class Monkey:
    id: int
    items: list[Item]
    operation: Callable
    test: MonkeyTest
    items_inspected: int = 0

    def append(self, item: Item):
        self.items.append(item)

    def round(self, game: "Game", divide=False, module=None):
        while self.items:
            self.items_inspected += 1
            item = self.items.pop(0)
            item.operation(self.operation)
            item.shrink(divide=divide, module=module)
            if self.test.test(item.worry_level):
                game[self.test.true].append(item)
            else:
                game[self.test.false].append(item)


@dataclass
class Game:
    monkeys: dict[int, Monkey]
    _module: Optional[int] = field(default=None, init=False, repr=False, compare=False)

    re_input: ClassVar[Pattern] = re.compile(
        r"Monkey\s(\d+):\n\s{2}Starting items:((?:(?:\s\d+),?)+)\n\s{2}Operation:\snew\s=\sold\s([+\-*.\/])\s(\d+|old)\n\s{2}Test:\sdivisible\sby\s(\d+)\n\s{4}If\strue:\sthrow\sto\smonkey\s(\d)\n\s{4}If\sfalse:\sthrow\sto\smonkey\s(\d)"
    )
    operator_mapping: ClassVar[dict[str, Callable]] = {
        "*": operator.mul,
        "-": operator.sub,
        "+": operator.add,
    }

    @property
    def module(self) -> int:
        if self._module is not None:
            return self._module
        self._module = math.lcm(*[x.test.test_number for x in self.monkeys.values()])
        return self._module

    def __getitem__(self, _id: int) -> Monkey:
        return self.monkeys[_id]

    @classmethod
    def yeild_monkey_definitios(cls, file: IO) -> Iterator[list[str]]:
        monkey_definitions = []
        for line in file:
            if line != "\n":
                monkey_definitions.append(line.strip())
            else:
                yield monkey_definitions
                monkey_definitions = []
        yield monkey_definitions

    @classmethod
    def _oper(cls, x: int, op: Callable) -> int:
        return op(x, x)

    @classmethod
    def setup(cls, file: IO) -> "Game":
        monkeys = {}
        values = cls.re_input.findall(file.read())
        for value in values:
            _id = int(value[0])
            _op = cls.operator_mapping[value[2]]
            items = list(map(Item, map(int, value[1].strip().split(","))))
            if value[3] == "old":
                op = partial(cls._oper, op=_op)
            else:
                op = partial(_op, int(value[3]))
            monkey = Monkey(
                id=_id,
                items=items,
                operation=op,
                test=MonkeyTest(
                    test_number=int(value[4]),
                    true=int(value[5]),
                    false=int(value[6]),
                ),
            )
            monkeys[_id] = monkey
        return Game(monkeys=monkeys)

    def print_round(self, round_number: int):
        print(f"### ROUND {round_number} ###")
        for monkey in self.monkeys.values():
            print(f"Monkey {monkey.id} inspected {monkey.items_inspected} items")

    def print_board(self, round_number: int):
        print(f"### ROUND {round_number} ###")
        for monkey in self.monkeys.values():
            print(
                f"Monkey {monkey.id} has items {', '.join(str(x.worry_level) for x in monkey.items)}"
            )

    def round(self, round_number, divide=False, debug=False):
        module = None
        if divide is False:
            module = self.module
        for monkey in self.monkeys.values():
            monkey.round(self, divide=divide, module=module)
        if debug is True:
            self.print_board(round_number)


def solver(
    input_path: Path, rounds: int, debug_when: Optional[Callable] = None, divide=False
) -> int:
    with input_path.open() as file:
        game: Game = Game.setup(file)
    for i in range(rounds):
        debug = False
        if debug_when is not None:
            debug = debug_when(i + 1)
        game.round(round_number=i + 1, divide=divide, debug=debug)
        if debug_when is not None and i == 1:
            game.print_board(round_number=i)
    items = sorted([x.items_inspected for x in game.monkeys.values()], reverse=True)
    solution = math.prod(items[:2])
    return solution


def main():
    input_path = Path("files/day11/test_input.txt")
    # input_path = Path("files/day11/input.txt")
    solution_1 = solver(input_path=input_path, rounds=20, divide=True)
    print(colored("Problem  1: ", "blue") + str(solution_1))
    solution_2 = solver(
        input_path=input_path,
        rounds=10000,
    )
    print(colored("Problem  2: ", "blue") + str(solution_2))


if __name__ == "__main__":
    main()
