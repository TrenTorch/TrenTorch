package main

import "fmt"

// O(len(tasks) + k) time where k is the number of distinct tasks, O(k) space
func leastInterval(tasks string, n int) int {
	if len(tasks) == 0 {
		return 0
	}
	counts := make(map[byte]int)
	for i := 0; i < len(tasks); i++ {
		counts[tasks[i]]++
	}
	m := 0
	for _, c := range counts {
		if c > m {
			m = c
		}
	}
	ties := 0
	for _, c := range counts {
		if c == m {
			ties++
		}
	}
	result := (m-1)*(n+1) + ties
	if len(tasks) > result {
		result = len(tasks)
	}
	return result
}

func main() {
	fmt.Println(leastInterval("AAABBB", 2))
}
