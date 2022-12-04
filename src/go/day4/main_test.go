package main

import (
	"testing"
)

func DataTest(ch chan string) {
	ch <- "2-4,6-8"
	ch <- "2-3,4-5"
	ch <- "5-7,7-9"
	ch <- "2-8,3-7"
	ch <- "6-6,4-6"
	ch <- "2-6,4-8"
	close(ch)
}

func TestProblem1(t *testing.T) {
	ch := make(chan string)
	go DataTest(ch)
	res := Problem1(ch)
	if res != 2 {
		t.Log("Should be 2, but got", res)
		t.Fail()
	}
}

func TestProblem2(t *testing.T) {
	ch := make(chan string)
	go DataTest(ch)
	res := Problem2(ch)
	if res != 4 {
		t.Log("Should be 4, but got", res)
		t.Fail()
	}
}
