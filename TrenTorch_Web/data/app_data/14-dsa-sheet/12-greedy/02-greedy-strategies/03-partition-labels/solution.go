package main

import "fmt"

// O(n) time, O(1) space (fixed 256-entry table), output size O(1) alphabet parts
func partitionLabels(s string) []int {
	var last [256]int
	for i := 0; i < len(s); i++ {
		last[s[i]] = i
	}
	sizes := []int{}
	start, end := 0, 0
	for i := 0; i < len(s); i++ {
		if last[s[i]] > end {
			end = last[s[i]]
		}
		if i == end {
			sizes = append(sizes, end-start+1)
			start = i + 1
		}
	}
	return sizes
}

func main() {
	fmt.Println(partitionLabels("ababcbacadefegdehijhklij"))
}
