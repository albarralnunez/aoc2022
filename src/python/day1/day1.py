from typing import Iterable


def yeild_elves_food(input_path) -> Iterable[list[int]]:
    """Generator of a file's lines."""
    with open(input_path, "r") as file:
        elf_food = []
        for line in file:
            if line != "\n":
                elf_food.append(int(line))
            else:
                yield elf_food
                elf_food = []


def problem_1(elves_food: Iterable[list[int]]) -> int:
    calored_per_elf: Iterable[int] = map(sum, elves_food)
    result = max(calored_per_elf)
    return result


def problem_2(elves_food: Iterable[list[int]]) -> int:
    calories_per_elf: Iterable[int] = map(sum, elves_food)
    result = sum(sorted(list(calories_per_elf), reverse=True)[:3])
    return result


def main():
    elves_food = yeild_elves_food("files/day1/input.txt")
    print(problem_1(elves_food))
    elves_food = yeild_elves_food("files/day1/input.txt")
    print(problem_2(elves_food))


if __name__ == "__main__":
    main()
