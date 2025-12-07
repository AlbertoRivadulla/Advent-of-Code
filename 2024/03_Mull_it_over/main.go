package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"

	"aoc_2024/lib"
)

func firstPart(inputFileName string) {
	defer lib.Timer("First part")()

	file, err := os.Open(inputFileName)
	if err != nil {
		fmt.Printf("Error opening file %v\n", inputFileName)
		os.Exit(1)
	}
	defer file.Close()

	pattern := `mul\((\d{1,3}),(\d{1,3})\)`
	re := regexp.MustCompile(pattern)

	scanner := bufio.NewScanner(file)

	sumMults := 0

	for scanner.Scan() {
		line := scanner.Text()

		matches := re.FindAllStringSubmatch(line, -1)

		for _, match := range matches {
			left, _ := strconv.Atoi(match[1])
			right, _ := strconv.Atoi(match[2])
			sumMults += left * right
		}
	}

	fmt.Printf("Sum of multiplications: %v\n", sumMults)
}

func secondPart(inputFileName string) {
	defer lib.Timer("Second part")()

	file, err := os.Open(inputFileName)
	if err != nil {
		fmt.Printf("Error opening file %v\n", inputFileName)
		os.Exit(1)
	}
	defer file.Close()

	pattern := `mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)`
	re := regexp.MustCompile(pattern)

	scanner := bufio.NewScanner(file)

	sumMults := 0

	do := true
	for scanner.Scan() {
		line := scanner.Text()

		matches := re.FindAllStringSubmatch(line, -1)

		for _, match := range matches {
			if match[0] == "do()" {
				do = true
			} else if match[0] == "don't()" {
				do = false
			} else {
				if do {
					left, _ := strconv.Atoi(match[1])
					right, _ := strconv.Atoi(match[2])
					sumMults += left * right
				}
			}
		}
	}

	fmt.Printf("Sum of multiplications: %v\n", sumMults)
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
