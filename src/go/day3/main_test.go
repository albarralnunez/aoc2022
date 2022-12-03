package main

import "testing"

func ChannelTestData(ch chan string) {
	ch <- "vJrwpWtwJgWrhcsFMMfFFhFp"
	ch <- "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"
	ch <- "PmmdzqPrVvPwwTWBwg"
	ch <- "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"
	ch <- "ttgJtRGJQctTZtZT"
	ch <- "CrZsJsPPZsGzwwsLwLmpwMDw"
	close(ch)

}

func TestGetId(t *testing.T) {
	res, err := GetId("swggwpJWwsWscJs", "DSLTJTmSVZJTBDZ")
	if err != nil {
		t.Log("error should be nil", err)
		t.Error(err)
	}
	if res != 'J' {
		t.Log("Should be J, but got", res)
		t.Fail()
	}
}

func TestIdToNumber(t *testing.T) {
	res := IdToNumber('A')
	if res != 27 {
		t.Log("Should be 27, but got", res)
		t.Fail()
	}
	res = IdToNumber('a')
	if res != 1 {
		t.Log("Should be 1, but got", res)
		t.Fail()
	}
}

func TestGetBadge(t *testing.T) {
	group := [3]string{
		"vJrwpWtwJgWrhcsFMMfFFhFp",
		"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
		"PmmdzqPrVvPwwTWBwg",
	}
	res, err := GetBadge(group[0], group[1], group[2])
	if err != nil {
		t.Log("error should be nil", err)
		t.Error(err)
	}
	if res != 'r' {
		t.Log("Should be r, but got", res)
		t.Fail()
	}

}

func TestProblem1(t *testing.T) {
	ch := make(chan string)
	go ChannelTestData(ch)
	res := Problem1(ch)
	if res != 157 {
		t.Log("Should be 157, but got", res)
		t.Fail()
	}
}

func TestProblem2(t *testing.T) {
	ch := make(chan string)
	go ChannelTestData(ch)
	res := Problem2(ch)
	if res != 70 {
		t.Log("Should be 70, but got", res)
		t.Fail()
	}
}
