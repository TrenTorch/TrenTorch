package main

import "fmt"

// nextTyped returns the index of the next character at or before i that
// survives backspaces, or -1 if none is left.
func nextTyped(text string, i int) int {
	skip := 0
	for i >= 0 {
		if text[i] == '#' {
			skip++
		} else if skip > 0 {
			skip--
		} else {
			return i
		}
		i--
	}
	return -1
}

// O(n + m) time, O(1) space
func backspaceCompare(s string, t string) bool {
	i, j := len(s)-1, len(t)-1
	for {
		i = nextTyped(s, i)
		j = nextTyped(t, j)
		if i < 0 && j < 0 {
			return true
		}
		if i < 0 || j < 0 || s[i] != t[j] {
			return false
		}
		i--
		j--
	}
}

func main() {
	fmt.Println(backspaceCompare("ab#c", "ad#c"))
}
