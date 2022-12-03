package main

import (
	"errors"
	"fmt"

	"github.com/albarralnunez/aoc2022/src/go/shared"
)

var GROUPSIZE int = 3

func SplitLineMiddle(line string) (string, string) {
	middle := len(line) / 2
	return line[:middle], line[middle:]
}

func GetId(line1, line2 string) (byte, error) {
	for i := 0; i < len(line1); i++ {
		for j := 0; j < len(line2); j++ {
			if line1[i] == line2[j] {
				return line1[i], nil
			}
		}
	}
	return byte(0), errors.New("no id found")
}

func GetBadge(elf1, elf2, elf3 string) (byte, error) {
	for i := 0; i < len(elf1); i++ {
		for j := 0; j < len(elf2); j++ {
			for k := 0; k < len(elf3); k++ {
				if elf1[i] == elf2[j] && elf2[j] == elf3[k] {
					return elf1[i], nil
				}
			}
		}
	}
	return byte(0), errors.New("no badge found")
}

func IdToNumber(id byte) int {
	/*
		a-z: 1-26
		A-Z: 27-52
	*/
	if id >= 'a' && id <= 'z' {
		return int(id - 'a' + 1)
	}
	if id >= 'A' && id <= 'Z' {
		return int(id - 'A' + 27)
	}
	return 0
}

func Problem1(ch chan string) int {
	res := 0
	for line := range ch {
		compartment1, compartment2 := SplitLineMiddle(line)
		rucksackid, err := GetId(compartment1, compartment2)
		if err != nil {
			panic(err)
		}
		res += IdToNumber(rucksackid)
	}
	return res
}

func YieldGroups(rucksacksch chan string, groupch chan [3]string) {
	var group [3]string
	for rucksack := range rucksacksch {
		group[0] = rucksack
		for i := 1; i < GROUPSIZE; i++ {
			group[i] = <-rucksacksch
		}
		groupch <- group
		group = [3]string{}
	}
	close(groupch)
}

func Problem2(rucksacksch chan string) int {
	res := 0
	groupch := make(chan [3]string)
	go YieldGroups(rucksacksch, groupch)
	for group := range groupch {
		badge, err := GetBadge(group[0], group[1], group[2])
		if err != nil {
			panic(err)
		}
		res += IdToNumber(badge)
	}
	return res
}

func main() {
	inputpath := "files/day3/input.txt"
	chP1 := make(chan string)
	go shared.StreamFileLines(chP1, inputpath)
	fmt.Println("Problem 1: ", Problem1(chP1))
	chP2 := make(chan string)
	go shared.StreamFileLines(chP2, inputpath)
	fmt.Println("Problem 2: ", Problem2(chP2))
}
