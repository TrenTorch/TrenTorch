package main

import (
	"fmt"
	"strconv"
	"strings"
)

func mustAtoi(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return v
}

// O(1) amortized time per operation, O(n) space for the hits
func runHitCounter(ops []string) []int {
	window := []int{}
	head := 0
	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		t := mustAtoi(parts[1])
		if parts[0] == "hit" {
			window = append(window, t)
		} else {
			for head < len(window) && window[head] <= t-300 {
				head++
			}
			out = append(out, len(window)-head)
		}
	}
	return out
}

func main() {
	fmt.Println(runHitCounter([]string{"hit 1", "hit 2", "hit 3", "count 4", "hit 300", "count 300", "count 301"}))
}
