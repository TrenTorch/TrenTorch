package main

import "fmt"

// O(n) time, O(n) space
func smallestRotation(s string) string {
	n := len(s)
	if n == 0 {
		return ""
	}
	s2 := s + s
	i, j, k := 0, 1, 0
	for i < n && j < n && k < n {
		a, b := s2[i+k], s2[j+k]
		if a == b {
			k++
			continue
		}
		if a > b {
			i += k + 1
		} else {
			j += k + 1
		}
		if i == j {
			j++
		}
		k = 0
	}
	start := i
	if j < start {
		start = j
	}
	return s2[start : start+n]
}

func main() {
	fmt.Println(smallestRotation("bca"))
}
