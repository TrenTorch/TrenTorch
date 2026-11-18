package main

import "fmt"

// O(n) time, O(1) space (alphabet bounded by 256 byte values)
func isomorphicStrings(s string, t string) bool {
	if len(s) != len(t) {
		return false
	}
	forward := map[byte]byte{}
	backward := map[byte]byte{}
	for i := 0; i < len(s); i++ {
		a, b := s[i], t[i]
		if mapped, ok := forward[a]; ok {
			if mapped != b {
				return false
			}
		} else {
			forward[a] = b
		}
		if mapped, ok := backward[b]; ok {
			if mapped != a {
				return false
			}
		} else {
			backward[b] = a
		}
	}
	return true
}

func main() {
	fmt.Println(isomorphicStrings("egg", "add"))
}
