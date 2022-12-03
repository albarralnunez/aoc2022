package main

import (
	"fmt"
	"strings"

	"github.com/albarralnunez/aoc2022/src/go/shared"
)

var scores = map[string]int{
	"A": 1,
	"B": 2,
	"C": 3,
}

var gameWinnerP1 = map[string]string{
	"A": "C",
	"B": "A",
	"C": "B",
}

var normalizeP1 = map[string]string{
	"X": "A",
	"Y": "B",
	"Z": "C",
}

var scoresMoveP2 = map[string]int{
	"X": 0,
	"Y": 3,
	"Z": 6,
}

var scoreP2 = map[string]map[string]int{
	"X": {
		"A": scores["C"],
		"B": scores["A"],
		"C": scores["B"],
	},
	"Y": {
		"A": scores["A"],
		"B": scores["B"],
		"C": scores["C"],
	},
	"Z": {
		"A": scores["B"],
		"B": scores["C"],
		"C": scores["A"],
	},
}

func RoundScore(player1 string, player2 string) int {
	if player1 == player2 {
		return 3
	} else if gameWinnerP1[player2] == player1 {
		return 6
	} else {
		return 0
	}
}

func Problem1(ch chan string) int {
	score := 0
	for line := range ch {
		move := strings.Split(line, " ")
		myPlayNormalize := normalizeP1[move[1]]
		score += scores[myPlayNormalize]
		score += RoundScore(move[0], myPlayNormalize)
	}
	return score
}

func Problem2(ch chan string) int {
	totalscore := 0
	for line := range ch {
		move := strings.Split(line, " ")
		score := scoresMoveP2[move[1]]
		totalscore += score
		totalscore += scoreP2[move[1]][move[0]]
	}
	return totalscore
}

func main() {
	inputpath := "files/day2/input.txt"
	// input_path := "src/go/day2/test.txt"
	chP1 := make(chan string)
	go shared.StreamFileLines(chP1, inputpath)
	fmt.Println(Problem1(chP1))
	chp2 := make(chan string)
	go shared.StreamFileLines(chp2, inputpath)
	fmt.Println(Problem2(chp2))
}
