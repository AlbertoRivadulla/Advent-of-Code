package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"aoc_2024/lib"
)

func getReports(inputFileName string) [][]int {
	file, err := os.Open(inputFileName)
	if err != nil {
		fmt.Printf("Error opening file %v\n", inputFileName)
		os.Exit(1)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var reports [][]int
	for scanner.Scan() {
		line := scanner.Text()

		fields := strings.Fields(line)

		var thisReport []int
		for _, field := range fields {
			thisNr, err := strconv.Atoi(field)
			if err != nil {
				fmt.Printf("Error: Not able to convert %v to an int", field)
			}

			thisReport = append(thisReport, thisNr)
		}

		reports = append(reports, thisReport)
	}

	return reports
}

func isValid(report []int) bool {
	if report[0] == report[1] {
		// Not valid
		return false
	}

	valid := true
	increasing := report[1] > report[0]
	for i := 0; i < len(report) - 1; i++ {
		if increasing {
			if report[i+1] < report[i] + 1 || report[i+1] > report[i] + 3 {
				valid = false
				break
			}
		} else {
			if report[i+1] > report[i] - 1 || report[i+1] < report[i] - 3 {
				valid = false
				break
			}
		}
	}

	return valid
}

func firstPart(inputFileName string) {
	defer lib.Timer("First part")()

	reports := getReports(inputFileName)

	nrValid := 0
	for _, report := range reports {

		if isValid(report) {
			nrValid++
		}
	}

	fmt.Printf("Number of valid reports: %v\n", nrValid)
}

func secondPart(inputFileName string) {
	defer lib.Timer("Second part")()

	reports := getReports(inputFileName)

	nrValid := 0
	for _, report := range reports {
		for ignored := -1; ignored < len(report); ignored++ {
			thisReport := []int {}

			for i := 0; i < len(report); i++ {
				if i == ignored {
					continue
				}

				thisReport = append(thisReport, report[i])
			}

			if isValid(thisReport) {
				nrValid++
				break
			}
		}
	}

	fmt.Printf("Number of valid reports: %v\n", nrValid)
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
