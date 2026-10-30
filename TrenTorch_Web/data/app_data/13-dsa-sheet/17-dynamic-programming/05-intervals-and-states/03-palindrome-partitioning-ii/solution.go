package main

import "fmt"

// O(n^2) time, O(n) space
func minCutPalindromes(s string) int {
	n := len(s)
	if n == 0 {
		return 0
	}
	cuts := make([]int, n+1) // cuts[i]: fewest cuts for the first i letters
	for i := range cuts {
		cuts[i] = i - 1
	}
	for centre := 0; centre < n; centre++ {
		pairs := [2][2]int{{centre, centre}, {centre, centre + 1}}
		for _, pair := range pairs {
			left, right := pair[0], pair[1]
			for left >= 0 && right < n && s[left] == s[right] {
				if cuts[left]+1 < cuts[right+1] {
					cuts[right+1] = cuts[left] + 1
				}
				left--
				right++
			}
		}
	}
	return cuts[n]
}

func main() {
	fmt.Println(minCutPalindromes("aab"))
}
