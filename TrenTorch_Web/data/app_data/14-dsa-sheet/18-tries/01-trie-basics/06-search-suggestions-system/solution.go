package main

import (
	"fmt"
	"sort"
	"strings"
)

// O(P log P + W * log P) time, where P = len(products) and W = len(searchWord); O(P) space
func suggestedProducts(products []string, searchWord string) [][]string {
	sorted := make([]string, len(products))
	copy(sorted, products)
	sort.Strings(sorted)
	out := make([][]string, 0, len(searchWord))
	for i := 1; i <= len(searchWord); i++ {
		prefix := searchWord[:i]
		start := sort.SearchStrings(sorted, prefix)
		end := min(start+3, len(sorted))
		suggestions := []string{}
		for _, p := range sorted[start:end] {
			if strings.HasPrefix(p, prefix) {
				suggestions = append(suggestions, p)
			}
		}
		out = append(out, suggestions)
	}
	return out
}

func main() {
	fmt.Println(suggestedProducts([]string{"mobile", "mouse", "moneypot", "monitor", "mousepad"}, "mouse"))
}
