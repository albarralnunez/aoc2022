package main
import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

func readInput(input_path string) string {
	/* Read string in the input file and return a string */
	input, err := ioutil.ReadFile(input_path)
	if err != nil {
		log.Fatal(err)
	}
	return string(input)
}

func createGrups(input string, chunk_size int) []string {
	/* Create a list of groups from the input consecutive*/
	var groups []string
	for i := 0; i < len(input)-chunk_size; i += 1{
		groups = append(groups, input[i:i+chunk_size])
	}
	return groups

}

func isAllDifferent(group string) bool {
	/* Check if all the answers in the group are different */
	for i, char := range group {
		if strings.Contains(group[i+1:], string(char)) {
			return false
		}
	}
	return true
}

func solver(input string, chunk_size int) int {
	/* Solve part 1 of the problem */
	var groups = createGrups(input, chunk_size)
	count := chunk_size
	for _, group := range groups {
		if !isAllDifferent(group) {
			count += 1
		} else {
			break
		}
	}
	return count
}

func main() {
	input := readInput("files/day6/input.txt")
	fmt.Println("Part 1:", solver(input, 4))
	fmt.Println("Part 2:", solver(input, 14))
}
