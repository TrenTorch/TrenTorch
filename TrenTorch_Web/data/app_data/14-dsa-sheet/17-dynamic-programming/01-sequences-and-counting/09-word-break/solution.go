package main

import "fmt"

type trieNode struct {
	children map[byte]*trieNode
	end      bool
}

// O(n * W) time where W is the longest word, O(total word length) space
func wordBreak(s string, words []string) bool {
	root := &trieNode{children: map[byte]*trieNode{}}
	for _, word := range words {
		node := root
		for i := 0; i < len(word); i++ {
			ch := word[i]
			next, ok := node.children[ch]
			if !ok {
				next = &trieNode{children: map[byte]*trieNode{}}
				node.children[ch] = next
			}
			node = next
		}
		node.end = true
	}
	n := len(s)
	reachable := make([]bool, n+1)
	reachable[0] = true
	for i := 0; i < n; i++ {
		if !reachable[i] {
			continue
		}
		node := root
		for j := i; j < n; j++ {
			next, ok := node.children[s[j]]
			if !ok {
				break
			}
			node = next
			if node.end {
				reachable[j+1] = true
			}
		}
	}
	return reachable[n]
}

func main() {
	fmt.Println(wordBreak("leetcode", []string{"leet", "code"}))
}
