package main

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var (
	patEols  = regexp.MustCompile(`[\r\n]+`)
	pat2Eols = regexp.MustCompile(`[\r\n]{2}`)
)

/*
	Modified version of Go's builtin bufio.ScanLines to return strings separated by
	two newlines (instead of one). Returns a string without newlines in it, and trims
	spaces from start and end.
	https://github.com/golang/go/blob/master/src/bufio/scan.go#L344-L364
*/
func ScanTwoConsecutiveNewlines(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}

	if loc := pat2Eols.FindIndex(data); loc != nil && loc[0] >= 0 {
		// Replace newlines within string with a space
		s := patEols.ReplaceAll(data[0:loc[0]+1], []byte(" "))
		// Trim spaces and newlines from string
		s = bytes.Trim(s, "\n ")
		return loc[1], s, nil
	}

	if atEOF {
		// Replace newlines within string with a space
		s := patEols.ReplaceAll(data, []byte(" "))
		// Trim spaces and newlines from string
		s = bytes.Trim(s, "\r\n ")
		return len(data), s, nil
	}

	// Request more data.
	return 0, nil, nil
}

func ReadFile(ch chan string, pathName string) {
	file, err := os.Open(pathName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(ScanTwoConsecutiveNewlines)

	for scanner.Scan() {
		line := scanner.Text()
		ch <- line
	}
	close(ch)
}

func Problem1(ch chan string) int {
	max := 0
	for line := range ch {
		numbers := strings.Split(line, " ")
		elfcal := 0
		for _, number_str := range numbers {
			number, err := strconv.Atoi(number_str)
			if err != nil {
				log.Fatal(err)
			}
			elfcal += number
		}
		if elfcal > max {
			max = elfcal
		}
	}
	return max
}

func Problem2(ch chan string) int {
	var elfscal []int
	for line := range ch {
		elfcal := 0
		numbers := strings.Split(line, " ")
		for _, numberStr := range numbers {
			number, err := strconv.Atoi(numberStr)
			if err != nil {
				log.Fatal(err)
			}
			elfcal += number
		}
		elfscal = append(elfscal, elfcal)
	}
	sort.Sort(sort.Reverse(sort.IntSlice(elfscal)))
	result := 0
	for _, elfcal := range elfscal[0:3] {
		result += elfcal
	}
	return result
}

func main() {
	chP1 := make(chan string)
	go ReadFile(chP1, "src/go/day1/input.txt")
	problem1 := Problem1(chP1)
	fmt.Println(problem1)
	chP2 := make(chan string)
	go ReadFile(chP2, "src/go/day1/input.txt")
	problem2 := Problem2(chP2)
	fmt.Println(problem2)
}
