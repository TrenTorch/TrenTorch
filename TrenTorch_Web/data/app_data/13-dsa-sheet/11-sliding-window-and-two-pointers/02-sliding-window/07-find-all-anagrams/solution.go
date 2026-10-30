package main

import "fmt"

// O(n) time, O(n) space for the output (fixed 26-letter arrays otherwise)
func findAnagrams(s string, p string) []int {
	m := len(p)
	if m == 0 || m > len(s) {
		return []int{}
	}
	var need, window [26]int
	for i := 0; i < m; i++ {
		need[p[i]-'a']++
	}
	out := []int{}
	for i := 0; i < len(s); i++ {
		window[s[i]-'a']++
		if i >= m {
			window[s[i-m]-'a']--
		}
		if i >= m-1 && window == need {
			out = append(out, i-m+1)
		}
	}
	return out
}

func main() {
	fmt.Println(findAnagrams("cbaebabacd", "abc"))
}
