package main

import "fmt"

// O(|a| * |b|) time, O(|b|) space
func isInterleave(a string, b string, c string) bool {
	if len(a)+len(b) != len(c) {
		return false
	}
	row := make([]bool, len(b)+1)
	row[0] = true
	for j := 1; j <= len(b); j++ {
		row[j] = row[j-1] && b[j-1] == c[j-1]
	}
	for i := 1; i <= len(a); i++ {
		row[0] = row[0] && a[i-1] == c[i-1]
		for j := 1; j <= len(b); j++ {
			row[j] = (row[j] && a[i-1] == c[i+j-1]) || (row[j-1] && b[j-1] == c[i+j-1])
		}
	}
	return row[len(b)]
}

func main() {
	fmt.Println(isInterleave("aabcc", "dbbca", "aadbbcbcac"))
}
