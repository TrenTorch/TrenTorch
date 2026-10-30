package main

import (
	"fmt"
	"sort"
)

// O(n) time, O(n) space
func repeatedDna(s string) []string {
	seen := make(map[string]bool)
	repeated := make(map[string]bool)
	for i := 0; i+10 <= len(s); i++ {
		part := s[i : i+10]
		if seen[part] {
			repeated[part] = true
		} else {
			seen[part] = true
		}
	}
	out := make([]string, 0, len(repeated))
	for part := range repeated {
		out = append(out, part)
	}
	sort.Strings(out)
	return out
}

func main() {
	fmt.Println(repeatedDna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"))
}
