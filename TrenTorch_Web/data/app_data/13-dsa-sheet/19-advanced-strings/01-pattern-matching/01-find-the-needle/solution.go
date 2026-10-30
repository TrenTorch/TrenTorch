package main

import "fmt"

// O(H + N) time, O(N) space (KMP)
func findNeedle(haystack string, needle string) int {
	if len(needle) == 0 {
		return 0
	}
	fail := make([]int, len(needle))
	k := 0
	for i := 1; i < len(needle); i++ {
		for k > 0 && needle[i] != needle[k] {
			k = fail[k-1]
		}
		if needle[i] == needle[k] {
			k++
		}
		fail[i] = k
	}
	k = 0
	for i := 0; i < len(haystack); i++ {
		ch := haystack[i]
		for k > 0 && ch != needle[k] {
			k = fail[k-1]
		}
		if ch == needle[k] {
			k++
		}
		if k == len(needle) {
			return i - k + 1
		}
	}
	return -1
}

func main() {
	fmt.Println(findNeedle("sadbutsad", "sad"))
}
