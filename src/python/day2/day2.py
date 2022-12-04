from typing import Iterator


SCORES = {
    "A": 1,
    "B": 2,
    "C": 3,
}

GAME_WINNER_P1 = {
    "A": "C",
    "B": "A",
    "C": "B",
}


NORMALIZE_P1 = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

SCORES_MOVE_P2 = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

SOCRE_P2 = {
    "X": {
        "A": SCORES["C"],
        "B": SCORES["A"],
        "C": SCORES["B"],
    },
    "Y": {
        "A": SCORES["A"],
        "B": SCORES["B"],
        "C": SCORES["C"],
    },
    "Z": {
        "A": SCORES["B"],
        "B": SCORES["C"],
        "C": SCORES["A"],
    },
}


def round_score(openent: str, myself: str) -> int:
    """Return the score of a round."""
    if openent == myself:
        return 3
    elif GAME_WINNER_P1[myself] == openent:
        return 6
    else:
        return 0


def total_round_score_p1(openent: str, myself: str) -> int:
    """Return the score of a game."""
    score = SCORES[myself]
    score += round_score(openent, myself)
    return score


def total_round_score_p2(oponent: str, result: str) -> int:
    """Return the score of a game."""
    score = SCORES_MOVE_P2[result]
    score += SOCRE_P2[result][oponent]
    return score


def yeild_round(input_path) -> Iterator[str]:
    """Generator of a file's lines."""
    with open(input_path, "r") as file:
        for rucksack in file:
            yield rucksack.strip()


def problem_1(rounds: Iterator[str]) -> int:
    normalized_game: Iterator[tuple[str, str]] = map(
        lambda x: (x[0], NORMALIZE_P1[x[1]]), map(lambda x: x.split(" "), rounds)
    )
    scores = map(lambda x: total_round_score_p1(*x), normalized_game)
    return sum(scores)


def problem_2(rounds: Iterator[str]) -> int:
    scores = map(
        lambda x: total_round_score_p2(*x), map(lambda x: x.split(" "), rounds)
    )
    return sum(scores)


def main():
    rucksacks = yeild_round("files/day2/input.txt")
    print(problem_1(rucksacks))
    rucksacks = yeild_round("files/day2/input.txt")
    print(problem_2(rucksacks))


if __name__ == "__main__":
    main()
