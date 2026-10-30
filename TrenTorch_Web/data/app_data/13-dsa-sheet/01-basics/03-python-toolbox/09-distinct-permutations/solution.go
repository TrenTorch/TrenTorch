package main

import "fmt"

// O(n * n!) time, O(n) space beyond the output (backtracking over distinct letters).
func distinctPermutations(s string) []string {
	var counts [26]int
	for i := 0; i < len(s); i++ {
		counts[s[i]-'a']++
	}
	n := len(s)
	out := []string{}
	prefix := make([]byte, 0, n)
	var build func()
	build = func() {
		if len(prefix) == n {
			out = append(out, string(prefix))
			return
		}
		for c := 0; c < 26; c++ {
			if counts[c] > 0 {
				counts[c]--
				prefix = append(prefix, byte('a'+c))
				build()
				prefix = prefix[:len(prefix)-1]
				counts[c]++
			}
		}
	}
	build()
	return out
}

func main() {
	fmt.Println(distinctPermutations("abc"))
}
