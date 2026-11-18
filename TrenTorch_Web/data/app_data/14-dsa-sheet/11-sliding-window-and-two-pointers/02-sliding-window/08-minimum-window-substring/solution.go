package main

import "fmt"

// O(|s| + |t|) time, O(1) space (fixed 256-byte arrays)
func minWindow(s string, t string) string {
	if len(t) == 0 {
		return ""
	}
	var need, have [256]int
	missing := 0
	for i := 0; i < len(t); i++ {
		if need[t[i]] == 0 {
			missing++
		}
		need[t[i]]++
	}
	bestStart, bestLen := 0, len(s)+1
	left := 0
	for right := 0; right < len(s); right++ {
		ch := s[right]
		have[ch]++
		if need[ch] > 0 && have[ch] == need[ch] {
			missing--
		}
		for missing == 0 {
			if right-left+1 < bestLen {
				bestStart, bestLen = left, right-left+1
			}
			gone := s[left]
			have[gone]--
			if need[gone] > 0 && have[gone] < need[gone] {
				missing++
			}
			left++
		}
	}
	if bestLen <= len(s) {
		return s[bestStart : bestStart+bestLen]
	}
	return ""
}

func main() {
	fmt.Println(minWindow("ADOBECODEBANC", "ABC"))
}
