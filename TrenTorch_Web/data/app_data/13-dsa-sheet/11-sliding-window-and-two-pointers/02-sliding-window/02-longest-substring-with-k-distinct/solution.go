package main

import "fmt"

// O(n) time, O(1) space (alphabet bounded by 256 byte values)
func longestKDistinct(s string, k int) int {
	count := make(map[byte]int)
	left := 0
	best := 0
	for right := 0; right < len(s); right++ {
		ch := s[right]
		count[ch]++
		for len(count) > k {
			count[s[left]]--
			if count[s[left]] == 0 {
				delete(count, s[left])
			}
			left++
		}
		if right-left+1 > best {
			best = right - left + 1
		}
	}
	return best
}

func main() {
	fmt.Println(longestKDistinct("eceba", 2))
}
