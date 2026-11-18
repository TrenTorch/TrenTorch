package main

import "fmt"

// O(n^2) precompute plus O(n * 2^n) enumeration time, O(n^2) space
func palindromePartitions(s string) [][]string {
	n := len(s)
	pal := make([][]bool, n)
	for i := range pal {
		pal[i] = make([]bool, n)
	}
	for length := 1; length <= n; length++ {
		for i := 0; i+length <= n; i++ {
			j := i + length - 1
			pal[i][j] = s[i] == s[j] && (length <= 2 || pal[i+1][j-1])
		}
	}
	out := [][]string{}
	var pieces []string
	var rec func(start int)
	rec = func(start int) {
		if start == n {
			out = append(out, append([]string(nil), pieces...))
			return
		}
		for j := start; j < n; j++ {
			if pal[start][j] {
				pieces = append(pieces, s[start:j+1])
				rec(j + 1)
				pieces = pieces[:len(pieces)-1]
			}
		}
	}
	rec(0)
	return out
}

func main() {
	fmt.Println(palindromePartitions("aab"))
}
