package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"aoc_2024/lib"
)

func getNumbers(inputFileName string) ([]int, []int) {
	file, err := os.Open(inputFileName)
	if err != nil {
		fmt.Printf("Error opening file %v\n", inputFileName)
		os.Exit(1)
	}
	defer file.Close()

	var leftNrs []int
	var rightNrs []int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		if strings.TrimSpace(line) == "" {
			// Skip empty lines
			continue
		}

		fields := strings.Fields(line)
		if len(fields) != 2 {
			fmt.Printf("Warning: The following line does not have two entries: %v\n", line)
			continue
		}

		leftNr, err := strconv.Atoi(fields[0])
		if err != nil {
			fmt.Printf("Error parsing number %v\n", fields[0])
			continue
		}
		rightNr, err := strconv.Atoi(fields[1])
		if err != nil {
			fmt.Printf("Error parsing number %v\n", fields[1])
			continue
		}

		leftNrs = append(leftNrs, leftNr)
		rightNrs = append(rightNrs, rightNr)
	}

	if len(leftNrs) != len(rightNrs) {
		fmt.Printf("Error: The length of the two arrays is different\n")
		os.Exit(1)
	}

	return leftNrs, rightNrs
}

func firstPart(inputFileName string) {
	defer lib.Timer("First part")()

	leftNrs, rightNrs := getNumbers(inputFileName)

	leftNrs = lib.QuickSort(leftNrs)
	rightNrs = lib.QuickSort(rightNrs)

	distance := 0
	for i := 0; i < len(leftNrs); i++ {
		distance += lib.Abs(leftNrs[i] - rightNrs[i])
	}

	fmt.Printf("Total distance: %v\n", distance)
}

func getSimilarity(leftNrs []int, rightNrs []int) int {
	leftNrs = lib.QuickSort(leftNrs)
	rightNrs = lib.QuickSort(rightNrs)

	similarity := 0

	leftIdx := 0
	rightIdx := 0
	currNr := leftNrs[0]
	thisSimilarity := 0
	for ; leftIdx < len(leftNrs); leftIdx++ {
		if leftNrs[leftIdx] == currNr {
			similarity += thisSimilarity
			continue
		}

		currNr = leftNrs[leftIdx]
		thisSimilarity = 0
		for rightNrs[rightIdx] <= currNr {
			if rightNrs[rightIdx] == currNr {
				thisSimilarity += currNr
			}

			rightIdx++
			
			if rightIdx == len(rightNrs) {
				rightIdx--
				break
			}
		}
		similarity += thisSimilarity
	}

	return similarity
}

func secondPart(inputFileName string) {
	defer lib.Timer("Second part")()

	leftNrs, rightNrs := getNumbers(inputFileName)

	similarity := getSimilarity(leftNrs, rightNrs)

	fmt.Printf("Similarity score: %v\n", similarity)
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
