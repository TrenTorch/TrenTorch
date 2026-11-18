package main

import "fmt"

// O(|s| * |t|) time, O(|t|) space
func numDistinct(s string, t string) int {
	const mod = 1000000007
	row := make([]int, len(t)+1)
	row[0] = 1
	for i := 0; i < len(s); i++ {
		ch := s[i]
		for j := len(t); j > 0; j-- {
			if t[j-1] == ch {
				row[j] = (row[j] + row[j-1]) % mod
			}
		}
	}
	return row[len(t)]
}

func main() {
	fmt.Println(numDistinct("rabbbit", "rabbit"))
}
