package main

import (
	"fmt"
	"strconv"
	"strings"
)

// O(n^2) time, O(n) space
func kthPermutation(n int, k int) string {
	remaining := make([]int, n)
	for i := range remaining {
		remaining[i] = i + 1
	}
	k--
	fact := make([]int, n)
	fact[0] = 1
	for i := 1; i < n; i++ {
		fact[i] = fact[i-1] * i
	}
	var out strings.Builder
	for size := n - 1; size >= 0; size-- {
		index := k / fact[size]
		k %= fact[size]
		out.WriteString(strconv.Itoa(remaining[index]))
		remaining = append(remaining[:index], remaining[index+1:]...)
	}
	return out.String()
}

func main() {
	fmt.Println(kthPermutation(3, 3))
}
