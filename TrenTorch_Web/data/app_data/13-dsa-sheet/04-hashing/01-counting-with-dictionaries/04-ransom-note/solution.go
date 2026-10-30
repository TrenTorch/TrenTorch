package main

import "fmt"

// O(n + m) time, O(1) space
func ransomNote(note string, magazine string) bool {
	var avail [256]int
	for i := 0; i < len(magazine); i++ {
		avail[magazine[i]]++
	}
	for i := 0; i < len(note); i++ {
		avail[note[i]]--
		if avail[note[i]] < 0 {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(ransomNote("aab", "baa"))
}
