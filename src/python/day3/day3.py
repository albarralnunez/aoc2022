from typing import Iterator
from functools import reduce


def yeild_rucksacks(input_path) -> Iterator[str]:
    """Generator of a file's lines."""
    with open(input_path, "r") as file:
        for rucksack in file:
            yield rucksack.strip()


def yeild_elves_groups(rucksacks: Iterator[str], size: int) -> Iterator[list[str]]:
    """Slice iterator in groups of and arbitrary size"""
    group = []
    for rucksack in rucksacks:
        group.append(rucksack)
        if len(group) == size:
            yield group
            group = []


def get_compartments(rucksack: str) -> tuple[str, str]:
    "Splits string in half"
    return rucksack[: len(rucksack) // 2], rucksack[len(rucksack) // 2 :]


def find_identifier(compartment1: str, compartment2: str) -> str:
    return next(iter(set(compartment1) & set(compartment2)))


def find_badge(elves_group: list[str]) -> str:
    rucksack_sets: Iterator[set[str]] = map(set, elves_group)
    final_result: set[str] = reduce(lambda x, y: x.intersection(y), rucksack_sets)
    return next(iter(final_result))


def id_to_score(id: str) -> int:
    """
    a-z = 1-26
    A-Z = 27-52
    """
    if id.islower():
        return ord(id) - 96
    else:
        return ord(id) - 38


def problem_1(rucksacks: Iterator[str]) -> int:
    result = sum(
        map(
            id_to_score,
            map(lambda x: find_identifier(*x), map(get_compartments, rucksacks)),
        )
    )
    return result


def problem_2(rucksacks: Iterator[str]) -> int:
    return sum(
        map(
            id_to_score,
            map(find_badge, yeild_elves_groups(rucksacks, 3)),
        )
    )


def main():
    rucksacks = yeild_rucksacks("files/day3/input.txt")
    print(problem_1(rucksacks))
    rucksacks = yeild_rucksacks("files/day3/input.txt")
    print(problem_2(rucksacks))


if __name__ == "__main__":
    main()
