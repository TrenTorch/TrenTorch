package main

import (
	"fmt"
	"sort"
)

// O(n * L log L) time for n words of max length L, O(n * L) space
func groupAnagrams(words []string) [][]string {
	groups := map[string][]string{}
	for _, word := range words {
		b := []byte(word)
		sort.Slice(b, func(i, j int) bool { return b[i] < b[j] })
		key := string(b)
		groups[key] = append(groups[key], word)
	}
	out := make([][]string, 0, len(groups))
	for _, g := range groups {
		sort.Strings(g)
		out = append(out, g)
	}
	sort.Slice(out, func(i, j int) bool { return lessStringLists(out[i], out[j]) })
	return out
}

// lexicographic comparison of two string lists, like Python list comparison
func lessStringLists(a, b []string) bool {
	for i := 0; i < len(a) && i < len(b); i++ {
		if a[i] != b[i] {
			return a[i] < b[i]
		}
	}
	return len(a) < len(b)
}

func main() {
	fmt.Println(groupAnagrams([]string{"eat", "tea", "tan", "ate", "nat", "bat"}))
}
