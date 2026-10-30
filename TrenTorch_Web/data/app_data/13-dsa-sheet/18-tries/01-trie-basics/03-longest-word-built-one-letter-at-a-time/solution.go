package main

import "fmt"

// O(total characters) time, O(total characters) space
func longestWord(words []string) string {
	seen := map[string]bool{}
	byLength := map[int][]string{}
	for _, w := range words {
		if seen[w] {
			continue
		}
		seen[w] = true
		byLength[len(w)] = append(byLength[len(w)], w)
	}
	built := map[string]bool{"": true}
	best := ""
	for length := 1; ; length++ {
		var good []string
		for _, w := range byLength[length] {
			if built[w[:len(w)-1]] {
				good = append(good, w)
			}
		}
		if len(good) == 0 {
			return best
		}
		for _, w := range good {
			built[w] = true
		}
		m := good[0]
		for _, w := range good[1:] {
			if w < m {
				m = w
			}
		}
		best = m
	}
}

func main() {
	fmt.Println(longestWord([]string{"w", "wo", "wor", "worl", "world"}))
}
