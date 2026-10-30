package main

import "fmt"

// manacherRadii builds t = "#" + "#".join(s) + "#" and returns it with the
// Manacher radius of every position in t.
func manacherRadii(s string) ([]byte, []int) {
	n := len(s)
	t := make([]byte, 0, 2*n+1)
	t = append(t, '#')
	for i := 0; i < n; i++ {
		t = append(t, s[i], '#')
	}
	m := len(t)
	radius := make([]int, m)
	centre, right := 0, 0
	for i := 0; i < m; i++ {
		if i < right {
			radius[i] = min(right-i, radius[2*centre-i])
		}
		for i-radius[i]-1 >= 0 && i+radius[i]+1 < m && t[i-radius[i]-1] == t[i+radius[i]+1] {
			radius[i]++
		}
		if i+radius[i] > right {
			centre, right = i, i+radius[i]
		}
	}
	return t, radius
}

// O(n) time, O(n) space
func countPalindromicSubstrings(s string) int {
	_, radius := manacherRadii(s)
	total := 0
	for _, r := range radius {
		total += (r + 1) / 2
	}
	return total
}

func main() {
	fmt.Println(countPalindromicSubstrings("abc"))
}
