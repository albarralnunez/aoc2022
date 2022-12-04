package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/albarralnunez/aoc2022/src/go/shared"
)

func isFullyContained(start1 int, end1 int, start2 int, end2 int) bool {
	/* Evaluate if one of the ranges is fully contained in the other */
	if start2 >= start1 && end2 <= end1 {
		return true
	}
	if start1 >= start2 && end1 <= end2 {
		return true
	}
	return false
}

func isOverlapping(start1 int, end1 int, start2 int, end2 int) bool {
	/* Evaluate if the ranges overlap */
	if start1 > end2 || start2 > end1 {
		return false
	}
	return true
}

func CastRangesToInts(assigmenRangeElf1 []string, assigmenRangeElf2 []string) (int, int, int, int) {
	assigmenRangeStartElf1, err := strconv.Atoi(assigmenRangeElf1[0])
	if err != nil {
		panic(err)
	}
	assigmenRangeEndElf1, err := strconv.Atoi(assigmenRangeElf1[1])
	if err != nil {
		panic(err)
	}
	assigmenRangeStartElf2, err := strconv.Atoi(assigmenRangeElf2[0])
	if err != nil {
		panic(err)
	}
	assigmenRangeEndElf2, err := strconv.Atoi(assigmenRangeElf2[1])
	if err != nil {
		panic(err)
	}
	return assigmenRangeStartElf1, assigmenRangeEndElf1, assigmenRangeStartElf2, assigmenRangeEndElf2
}

func Problem1(ch chan string) int {
	result := 0
	for teamStr := range ch {
		team := strings.Split(teamStr, ",")
		assigmenRangeElf1 := strings.Split(team[0], "-")
		assigmenRangeElf2 := strings.Split(team[1], "-")
		assigmenRangeStartElf1, assigmenRangeEndElf1, assigmenRangeStartElf2, assigmenRangeEndElf2 := CastRangesToInts(assigmenRangeElf1, assigmenRangeElf2)
		if isFullyContained(assigmenRangeStartElf1, assigmenRangeEndElf1, assigmenRangeStartElf2, assigmenRangeEndElf2) {
			result++
		}
	}
	return result
}

func Problem2(ch chan string) int {
	result := 0
	for teamStr := range ch {
		team := strings.Split(teamStr, ",")
		assigmenRangeElf1 := strings.Split(team[0], "-")
		assigmenRangeElf2 := strings.Split(team[1], "-")
		assigmenRangeStartElf1, assigmenRangeEndElf1, assigmenRangeStartElf2, assigmenRangeEndElf2 := CastRangesToInts(assigmenRangeElf1, assigmenRangeElf2)
		if isOverlapping(assigmenRangeStartElf1, assigmenRangeEndElf1, assigmenRangeStartElf2, assigmenRangeEndElf2) {
			result++
		}
	}
	return result
}

func main() {
	inputpath := "files/day4/input.txt"
	chP1 := make(chan string)
	go shared.StreamFileLines(chP1, inputpath)
	fmt.Println("Problem 1:", Problem1(chP1))
	chP2 := make(chan string)
	go shared.StreamFileLines(chP2, inputpath)
	fmt.Println("Problem 2:", Problem2(chP2))
}
