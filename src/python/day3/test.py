import pytest

from src.python.day3.day3 import find_identifier, find_badge, problem_2


@pytest.mark.parametrize(
    "container1,container2,expected",
    (
        ("vJrwpWtwJgWr", "hcsFMMfFFhFp", "p"),
        ("PmmdzqPrV", "vPwwTWBwg", "P"),
    ),
)
def test_find_identifier(container1, container2, expected):
    assert find_identifier(container1, container2) == expected


@pytest.mark.parametrize(
    "group,expected",
    (
        (
            [
                "vJrwpWtwJgWrhcsFMMfFFhFp",
                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg",
            ],
            "r",
        ),
        (
            [
                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                "ttgJtRGJQctTZtZT",
                "CrZsJsPPZsGzwwsLwLmpwMDw",
            ],
            "Z",
        ),
    ),
)
def test_find_badge(group, expected):
    assert find_badge(group) == expected


def test_problem_2():
    rucksacks = iter(
        [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
        ]
    )
    res = problem_2(rucksacks)
    assert res == 70, f"Expected 70, got {res}"
