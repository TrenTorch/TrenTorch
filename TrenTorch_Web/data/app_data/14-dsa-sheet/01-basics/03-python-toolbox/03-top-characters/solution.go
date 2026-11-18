package main

import (
	"fmt"
	"sort"
)

// CharCount is one [character, count] pair.
type CharCount struct {
	Char  string
	Count int
}

// O(n + u log u) time, O(u) space where u is the number of distinct characters
func topCharacters(s string, k int) []CharCount {
	freq := make(map[rune]int)
	for _, ch := range s {
		freq[ch]++
	}
	ranked := make([]CharCount, 0, len(freq))
	for ch, n := range freq {
		ranked = append(ranked, CharCount{string(ch), n})
	}
	sort.Slice(ranked, func(i, j int) bool {
		if ranked[i].Count != ranked[j].Count {
			return ranked[i].Count > ranked[j].Count
		}
		return ranked[i].Char < ranked[j].Char
	})
	if k < 0 {
		k = 0
	}
	if k > len(ranked) {
		k = len(ranked)
	}
	return ranked[:k]
}

func main() {
	fmt.Println(topCharacters("abracadabra", 2))
}
