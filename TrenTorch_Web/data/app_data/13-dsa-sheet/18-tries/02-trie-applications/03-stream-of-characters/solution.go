package main

import "fmt"

// O(total word length * alphabet + len(stream)) amortized time, O(total word length) space
func streamChecker(words []string, stream string) []bool {
	gotoTbl := []map[byte]int{make(map[byte]int)}
	fail := []int{0}
	ends := []bool{false}
	for _, word := range words {
		node := 0
		for i := 0; i < len(word); i++ {
			ch := word[i]
			child, ok := gotoTbl[node][ch]
			if !ok {
				gotoTbl = append(gotoTbl, make(map[byte]int))
				fail = append(fail, 0)
				ends = append(ends, false)
				child = len(gotoTbl) - 1
				gotoTbl[node][ch] = child
			}
			node = child
		}
		ends[node] = true
	}
	queue := []int{}
	for _, child := range gotoTbl[0] {
		queue = append(queue, child)
	}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if ends[fail[node]] {
			ends[node] = true
		}
		for ch, child := range gotoTbl[node] {
			f := fail[node]
			for f != 0 {
				if _, ok := gotoTbl[f][ch]; ok {
					break
				}
				f = fail[f]
			}
			fail[child] = gotoTbl[f][ch]
			queue = append(queue, child)
		}
	}

	out := make([]bool, 0, len(stream))
	state := 0
	for i := 0; i < len(stream); i++ {
		ch := stream[i]
		for state != 0 {
			if _, ok := gotoTbl[state][ch]; ok {
				break
			}
			state = fail[state]
		}
		state = gotoTbl[state][ch]
		out = append(out, ends[state])
	}
	return out
}

func main() {
	fmt.Println(streamChecker([]string{"cd", "f", "kl"}, "abcdefghijkl"))
}
