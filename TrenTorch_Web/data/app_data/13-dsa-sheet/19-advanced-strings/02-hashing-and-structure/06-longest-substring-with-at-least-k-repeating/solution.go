package main

import "fmt"

// O(26 * n * depth) time worst case, O(n) recursion depth
func longestSubstringKRepeating(s string, k int) int {
	var solve func(lo, hi int) int
	solve = func(lo, hi int) int {
		if hi-lo < k {
			return 0
		}
		var counts [256]int
		for i := lo; i < hi; i++ {
			counts[s[i]]++
		}
		var rare [256]bool
		hasRare := false
		for c := 0; c < 256; c++ {
			if counts[c] > 0 && counts[c] < k {
				rare[c] = true
				hasRare = true
			}
		}
		if !hasRare {
			return hi - lo
		}
		best := 0
		start := lo
		for i := lo; i <= hi; i++ {
			if i == hi || rare[s[i]] {
				if r := solve(start, i); r > best {
					best = r
				}
				start = i + 1
			}
		}
		return best
	}
	return solve(0, len(s))
}

func main() {
	fmt.Println(longestSubstringKRepeating("aaabb", 3))
}
