package main

import (
	"testing"
)


func TestPart1(t *testing.T) {
	var tests = []struct {
        a string
		b, want int
    }{
		{"bvwbjplbgvbhsrlpgdmjqwftvncz", 4,5},
		{"nppdvjthqldpwncqszvftbrmjlhg", 4,6},
		{"nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4,10},
		{"zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4,11},
		{"mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14,19},
		{"bvwbjplbgvbhsrlpgdmjqwftvncz", 14, 23},
		{"nppdvjthqldpwncqszvftbrmjlhg", 14, 23},
		{"nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14, 29},
		{"zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14, 26},
	}
	for _, test := range tests {
		if got := solver(test.a, test.b); got != test.want {
			t.Errorf("solver(%q, %d) got %d want %d", test.a, test.b, got, test.want)
		}
	}
}