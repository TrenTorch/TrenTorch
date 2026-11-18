package main

import (
	"fmt"
	"strconv"
	"strings"
)

// O(n) time, O(n) space
func compressRuns(s string) string {
	var sb strings.Builder
	i := 0
	for i < len(s) {
		j := i
		for j < len(s) && s[j] == s[i] {
			j++
		}
		sb.WriteByte(s[i])
		if n := j - i; n > 1 {
			sb.WriteString(strconv.Itoa(n))
		}
		i = j
	}
	return sb.String()
}

func main() {
	fmt.Println(compressRuns("aabcccccaaa"))
}
