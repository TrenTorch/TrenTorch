package main

import "fmt"

// O(n * m) time, O(1) extra space (n words, m = prefix length)
func longestCommonPrefix(words []string) string {
	if len(words) == 0 {
		return ""
	}
	first, last := words[0], words[0]
	for _, w := range words[1:] {
		if w < first {
			first = w
		}
		if w > last {
			last = w
		}
	}
	i := 0
	for i < len(first) && i < len(last) && first[i] == last[i] {
		i++
	}
	return first[:i]
}

func main() {
	fmt.Println(longestCommonPrefix([]string{"flower", "flow", "flight"}))
}
