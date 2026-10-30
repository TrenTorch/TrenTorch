package main

import "fmt"

// O(len(a) * len(b)) time, O(min(len(a), len(b))) space
func editDistance(a string, b string) int {
	if len(b) > len(a) {
		a, b = b, a
	}
	prev := make([]int, len(b)+1)
	for j := range prev {
		prev[j] = j
	}
	for i := 1; i <= len(a); i++ {
		cur := make([]int, len(b)+1)
		cur[0] = i
		for j := 1; j <= len(b); j++ {
			if a[i-1] == b[j-1] {
				cur[j] = prev[j-1]
			} else {
				cur[j] = 1 + min(prev[j-1], prev[j], cur[j-1])
			}
		}
		prev = cur
	}
	return prev[len(b)]
}

func main() {
	fmt.Println(editDistance("horse", "ros"))
}
