package main

import "fmt"

// O(n) time, O(1) space (fixed 26-letter arrays)
func checkInclusion(s1 string, s2 string) bool {
	m := len(s1)
	if m > len(s2) {
		return false
	}
	var need, window [26]int
	for i := 0; i < m; i++ {
		need[s1[i]-'a']++
	}
	for i := 0; i < len(s2); i++ {
		window[s2[i]-'a']++
		if i >= m {
			window[s2[i-m]-'a']--
		}
		if i >= m-1 && window == need {
			return true
		}
	}
	return m == 0
}

func main() {
	fmt.Println(checkInclusion("ab", "eidbaooo"))
}
