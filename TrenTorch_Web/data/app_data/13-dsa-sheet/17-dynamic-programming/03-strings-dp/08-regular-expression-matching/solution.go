package main

import "fmt"

func fits(x byte, ch byte) bool {
	return x == '.' || x == ch
}

// O(|s| * |p|) time, O(|p|) space
func isMatchRegex(s string, p string) bool {
	prev := make([]bool, len(p)+1)
	prev[0] = true
	for j := 2; j <= len(p); j++ {
		prev[j] = p[j-1] == '*' && prev[j-2]
	}
	for i := 1; i <= len(s); i++ {
		cur := make([]bool, len(p)+1)
		for j := 1; j <= len(p); j++ {
			if p[j-1] == '*' {
				cur[j] = cur[j-2] || (fits(p[j-2], s[i-1]) && prev[j])
			} else {
				cur[j] = fits(p[j-1], s[i-1]) && prev[j-1]
			}
		}
		prev = cur
	}
	return prev[len(p)]
}

func main() {
	fmt.Println(isMatchRegex("aab", "c*a*b"))
}
