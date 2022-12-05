package main

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/albarralnunez/aoc2022/src/go/shared"
)

type Ship struct {
	stack [][]byte
}

func Reverse(input []byte) []byte {
	var output []byte

	for i := len(input) - 1; i >= 0; i-- {
		output = append(output, input[i])
	}

	return output
}

func (s Ship) Repr() string {
	repr := ""
	for i, stack := range s.stack {
		repr += strconv.Itoa(i+1) + " " + string(stack) + "\n"
	}
	return repr
}

func FindNumberOfStacks(s string) int {
	re := regexp.MustCompile(`\d+`)
	matches := re.FindAllString(s, -1)
	size, err := strconv.Atoi(matches[len(matches)-1])
	if err != nil {
		panic(err)
	}
	return size
}

func (s Ship) Setup(cargo_blueprint []string) Ship {
	last_line := cargo_blueprint[len(cargo_blueprint)-2]
	number_of_stacks := FindNumberOfStacks(last_line)
	s.stack = make([][]byte, number_of_stacks)
	cargo_blueprint_clean := cargo_blueprint[:len(cargo_blueprint)-2]
	re, e := regexp.Compile(`(\[\w\]\s?|\s{4})`)
	if e != nil {
		panic(e)
	}
	for _, line := range cargo_blueprint_clean {
		layer := re.FindAll([]byte(line), -1)
		for i, item := range layer {
			if item[0] != ' ' {
				s.stack[i] = append(s.stack[i], item[1])
			}
		}
	}
	for i, stack := range s.stack {
		s.stack[i] = Reverse(stack)
	}
	return s
}

func ReadBluepirnt(ch chan string) []string {
	var blueprint []string
	for line := range ch {
		blueprint = append(blueprint, line)
		if line == "" {
			break
		}
	}
	return blueprint
}

// 1, 2, 3
func SplitSliceByIndex(slice []byte, index int) ([]byte, []byte) {
	return slice[:len(slice)-index], slice[len(slice)-index:]
}

func (s Ship) MoveP1(size, from, to int, verbose bool) Ship {
	if verbose {
		fmt.Println("Moving", size, "from", from, "to", to)
	}
	remaining, stack_to_move := SplitSliceByIndex(s.stack[from-1], size)
	if verbose {
		fmt.Println("Stack to move:", string(stack_to_move))
	}
	s.stack[from-1] = remaining
	s.stack[to-1] = append(s.stack[to-1], Reverse(stack_to_move)...)
	return s
}

func (s Ship) MoveP2(size, from, to int, verbose bool) Ship {
	if verbose {
		fmt.Println("Moving", size, "from", from, "to", to)
	}
	remaining, stack_to_move := SplitSliceByIndex(s.stack[from-1], size)

	if verbose {
		fmt.Println("Stack to move:", string(stack_to_move))
	}
	s.stack[from-1] = remaining
	s.stack[to-1] = append(s.stack[to-1], stack_to_move...)
	return s
}

func (s Ship) GetStacksTops() []byte {
	result := make([]byte, len(s.stack))
	for i, stack := range s.stack {
		if len(stack) > 0 {
			result[i] = stack[len(stack)-1]
		} else {
			result[i] = ' '
		}
	}
	return result
}

func CastMatchesToIntegres(matches [][]string) []int {
	result := make([]int, len(matches))
	for i, match := range matches {
		result[i], _ = strconv.Atoi(match[0])
	}
	return result
}

func Solver(chP1 chan string, strategy int, verbose bool) string {
	re, e := regexp.Compile(`move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)`)
	if e != nil {
		panic(e)
	}
	cargo_blueprint := ReadBluepirnt(chP1)
	ship := Ship{}
	ship = ship.Setup(cargo_blueprint)
	if verbose {
		fmt.Println("Initial state:")
		fmt.Println(ship.Repr())
	}
	for instruction := range chP1 {
		matches := re.FindAllStringSubmatch(instruction, -1)
		size, _ := strconv.Atoi(matches[0][1])
		from, _ := strconv.Atoi(matches[0][2])
		to, _ := strconv.Atoi(matches[0][3])
		if strategy == 1 {
			ship = ship.MoveP1(size, from, to, verbose)
		} else {
			ship = ship.MoveP2(size, from, to, verbose)
		}
		if verbose {
			fmt.Println("Ship state:")
			fmt.Println(ship.Repr())
		}
	}
	return string(ship.GetStacksTops())
}

func main() {
	// inputpath := "files/day5/test_input.txt"
	inputpath := "files/day5/input.txt"
	verbose := false
	chP1 := make(chan string)
	go shared.StreamFileLines(chP1, inputpath)
	fmt.Println("Problem 1:")
	fmt.Println(Solver(chP1, 1, verbose))
	chP2 := make(chan string)
	go shared.StreamFileLines(chP2, inputpath)
	fmt.Println("Problem 2:")
	fmt.Println(Solver(chP2, 2, verbose))
}
