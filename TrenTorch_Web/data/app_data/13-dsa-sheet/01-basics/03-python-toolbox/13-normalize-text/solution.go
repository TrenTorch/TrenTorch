package main

import (
	"fmt"
	"strings"
)

// O(n) time, O(n) space (single pass; lower-cases ASCII letters and collapses separators).
func normalizeText(s string) string {
	var b strings.Builder
	pendingSpace := false
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= 'A' && c <= 'Z' {
			c += 'a' - 'A'
		}
		if (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') {
			if pendingSpace && b.Len() > 0 {
				b.WriteByte(' ')
			}
			pendingSpace = false
			b.WriteByte(c)
		} else {
			pendingSpace = true
		}
	}
	return b.String()
}

func main() {
	fmt.Println(normalizeText("  Hello,   World!! 42 "))
}
