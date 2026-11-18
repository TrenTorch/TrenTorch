package main

import (
	"fmt"
	"sort"
)

func isPalindrome(s string) bool {
	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
		if s[i] != s[j] {
			return false
		}
	}
	return true
}

func reverseString(s string) string {
	b := []byte(s)
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
	return string(b)
}

// O(N * L^2) time (N = len(words), L = max word length), O(total length) space
func palindromePairs(words []string) [][]int {
	index := map[string][]int{}
	for i, w := range words {
		index[w] = append(index[w], i)
	}
	found := map[[2]int]bool{}
	for i, w := range words {
		for cut := 0; cut <= len(w); cut++ {
			prefix, suffix := w[:cut], w[cut:]
			if isPalindrome(prefix) {
				for _, j := range index[reverseString(suffix)] {
					if j != i {
						found[[2]int{j, i}] = true
					}
				}
			}
			if isPalindrome(suffix) {
				for _, j := range index[reverseString(prefix)] {
					if j != i {
						found[[2]int{i, j}] = true
					}
				}
			}
		}
	}
	pairs := make([][]int, 0, len(found))
	for p := range found {
		pairs = append(pairs, []int{p[0], p[1]})
	}
	sort.Slice(pairs, func(a, b int) bool {
		if pairs[a][0] != pairs[b][0] {
			return pairs[a][0] < pairs[b][0]
		}
		return pairs[a][1] < pairs[b][1]
	})
	return pairs
}

func main() {
	fmt.Println(palindromePairs([]string{"abcd", "dcba", "lls", "s", "sssll"}))
}
