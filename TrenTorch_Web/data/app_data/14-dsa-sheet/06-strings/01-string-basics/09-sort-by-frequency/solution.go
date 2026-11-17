package main

import (
	"fmt"
	"sort"
	"strings"
)

// O(n + k log k) time, O(n) space (k = number of distinct characters)
func sortByFrequency(s string) string {
	counts := make(map[byte]int)
	for i := 0; i < len(s); i++ {
		counts[s[i]]++
	}
	order := make([]byte, 0, len(counts))
	for ch := range counts {
		order = append(order, ch)
	}
	sort.Slice(order, func(a, b int) bool {
		ca, cb := counts[order[a]], counts[order[b]]
		if ca != cb {
			return ca > cb
		}
		return order[a] < order[b]
	})
	var sb strings.Builder
	for _, ch := range order {
		for n := 0; n < counts[ch]; n++ {
			sb.WriteByte(ch)
		}
	}
	return sb.String()
}

func main() {
	fmt.Println(sortByFrequency("tree"))
}
