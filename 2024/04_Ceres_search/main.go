package main

import (
	"bufio"
	"fmt"
	"os"

	"aoc_2024/lib"
)

func readLines(inputFileName string) [][]rune {
	file, err := os.Open(inputFileName)
	if err != nil {
		fmt.Printf("Error opening file %v\n", inputFileName)
		os.Exit(1)
	}
	defer file.Close()

	lines := [][]rune{}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		thisLine := []rune{}
		for _, ch := range line {
			if ch != '\n' {
				thisLine = append(thisLine, ch)
			}
		}
		lines = append(lines, thisLine)
	}

	return lines
}

func countAppearances(lines [][]rune, wordStr string) int {
	appearances := 0

	var deltas = [][]int {
		{-1, 0},
		{-1, 1},
		{0, 1},
		{1, 1},
		{1, 0},
		{1, -1},
		{0, -1},
		{-1, -1},
	}

	word := []rune(wordStr)

	for i := range len(lines) {
		for j := range len(lines[i]) {
			for _, delta := range deltas {
				currI := i
				currJ := j
				valid := true
				for wordIdx := range len(word) {
					if currI < 0 || currI >= len(lines) || currJ < 0 || currJ >= len(lines[i]) {
						valid = false
						break
					}
					if lines[currI][currJ] != word[wordIdx] {
						valid = false
						break
					}

					currI += delta[0]
					currJ += delta[1]
				}
				if valid {
					appearances++
				}
			}
		}
	}

	return appearances
}

func firstPart(inputFileName string) {
	defer lib.Timer("First part")()

	lines := readLines(inputFileName)

	appearances := countAppearances(lines, "XMAS")

	fmt.Printf("Appearances of XMAS %v\n", appearances)
}

type Appearance struct {
	i int
	j int
	deltaIdx int
}

func countCrossedAppearances(lines [][]rune, wordStr string) int {
	var deltas = [][]int {
		{-1, 0},
		{-1, 1},
		{0, 1},
		{1, 1},
		{1, 0},
		{1, -1},
		{0, -1},
		{-1, -1},
	}

	word := []rune(wordStr)

	appearances := []Appearance{}

	for i := range len(lines) {
		for j := range len(lines[i]) {
			for deltaIdx, delta := range deltas {
				currI := i
				currJ := j
				valid := true
				for wordIdx := range len(word) {
					if currI < 0 || currI >= len(lines) || currJ < 0 || currJ >= len(lines[i]) {
						valid = false
						break
					}
					if lines[currI][currJ] != word[wordIdx] {
						valid = false
						break
					}

					currI += delta[0]
					currJ += delta[1]
				}
				if valid {
					appearances = append(appearances, 
						Appearance{
							i: i,
							j: j,
							deltaIdx: deltaIdx,
						})
				}
			}
		}
	}

	// Count the crossed appearances
	crossedAppearances := 0
	for i, app1 := range appearances[:len(appearances) - 1] {
		for _, app2 := range appearances[i+1:] {
			if app1.i == app2.i && app1.j == app2.j {
				if app1.deltaIdx == app2.deltaIdx {
				}
			}
			if app1.i + deltas[app1.deltaIdx][0] == app2.i + deltas[app2.deltaIdx][0] &&
				app1.j + deltas[app1.deltaIdx][1] == app2.j + deltas[app2.deltaIdx][1] && 
				lib.Abs(app1.deltaIdx - app2.deltaIdx) % 2 == 0 &&
				(app1.deltaIdx + 1) % 2 == 0 &&
				(app2.deltaIdx + 1) % 2 == 0 {
				crossedAppearances++
			}
		}

	}

	return crossedAppearances
}

func secondPart(inputFileName string) {
	defer lib.Timer("Second part")()

	lines := readLines(inputFileName)

	appearances := countCrossedAppearances(lines, "MAS")

	fmt.Printf("Crossed appearances of MAS %v\n", appearances)
}

func main() {
	fmt.Println()

	if len(os.Args) < 2 {
		fmt.Println("Usage:\n\t./main <input_file>")
		os.Exit(1)
	}

	inputFileName := os.Args[1]

	firstPart(inputFileName)

	secondPart(inputFileName)
}
