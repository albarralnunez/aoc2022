package shared

import (
	"bufio"
	"log"
	"os"
)

func StreamFileLines(ch chan<- string, pathName string) {
	file, err := os.Open(pathName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		ch <- line
	}
	close(ch)
}
