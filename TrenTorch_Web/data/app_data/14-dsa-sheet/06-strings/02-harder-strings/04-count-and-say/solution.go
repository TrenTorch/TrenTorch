package main

import (
	"fmt"
	"strconv"
)

// O(L * n) time where L is the length of the final term, O(L) space
func countAndSay(n int) string {
	term := []byte("1")
	for k := 0; k < n-1; k++ {
		next := make([]byte, 0, 2*len(term))
		for i := 0; i < len(term); {
			j := i
			for j < len(term) && term[j] == term[i] {
				j++
			}
			next = strconv.AppendInt(next, int64(j-i), 10)
			next = append(next, term[i])
			i = j
		}
		term = next
	}
	return string(term)
}

func main() {
	fmt.Println(countAndSay(4))
}
