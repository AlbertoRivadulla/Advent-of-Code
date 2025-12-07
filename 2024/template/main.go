package main

import (
	"bufio"
	"fmt"
	"os"

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

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		fmt.Printf("Line %v\n", line)
	}

	// TODO:
}

func secondPart(inputFileName string) {
	defer lib.Timer("Second part")()

	// TODO:
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
