package lib

import (
	"fmt"
	"time"
)

func Timer(name string) func() {
	start := time.Now()

	return func() {
		fmt.Printf("\n[TIMER] %s took %v\n\n", name, time.Since(start))
	}
}

