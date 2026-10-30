package main

import "fmt"

type ladderItem struct {
	word  string
	steps int
}

// O(N * L^2) time, O(N * L) space (N words, word length L)
func ladderLength(begin string, end string, words []string) int {
	allowed := make(map[string]bool, len(words))
	for _, w := range words {
		allowed[w] = true
	}
	if !allowed[end] {
		return 0
	}
	allowed[begin] = true
	groups := make(map[string][]string)
	for w := range allowed {
		for i := 0; i < len(w); i++ {
			key := w[:i] + "*" + w[i+1:]
			groups[key] = append(groups[key], w)
		}
	}
	seen := map[string]bool{begin: true}
	queue := []ladderItem{{begin, 1}}
	for head := 0; head < len(queue); head++ {
		cur := queue[head]
		if cur.word == end {
			return cur.steps
		}
		for i := 0; i < len(cur.word); i++ {
			key := cur.word[:i] + "*" + cur.word[i+1:]
			for _, other := range groups[key] {
				if !seen[other] {
					seen[other] = true
					queue = append(queue, ladderItem{other, cur.steps + 1})
				}
			}
		}
	}
	return 0
}

func main() {
	fmt.Println(ladderLength("hit", "cog", []string{"hot", "dot", "dog", "lot", "log", "cog"}))
}
