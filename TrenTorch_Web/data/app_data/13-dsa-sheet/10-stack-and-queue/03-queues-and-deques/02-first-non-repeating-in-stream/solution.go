package main

import "fmt"

// O(n) time, O(n) space
func firstNonRepeatingStream(s string) string {
	counts := make(map[byte]int)
	queue := []byte{}
	head := 0
	out := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		ch := s[i]
		counts[ch]++
		if counts[ch] == 1 {
			queue = append(queue, ch)
		}
		for head < len(queue) && counts[queue[head]] > 1 {
			head++
		}
		if head < len(queue) {
			out = append(out, queue[head])
		} else {
			out = append(out, '#')
		}
	}
	return string(out)
}

func main() {
	fmt.Println(firstNonRepeatingStream("aabc"))
}
