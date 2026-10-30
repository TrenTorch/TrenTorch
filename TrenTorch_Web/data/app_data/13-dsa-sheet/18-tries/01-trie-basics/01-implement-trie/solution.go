package main

import (
	"fmt"
	"strings"
)

type trieNode struct {
	children map[byte]*trieNode
	end      bool
}

func newTrieNode() *trieNode {
	return &trieNode{children: map[byte]*trieNode{}}
}

// O(L) time per operation (L = word length), O(total inserted length) space
func runTrie(ops []string) []bool {
	root := newTrieNode()
	walk := func(word string) *trieNode {
		node := root
		for i := 0; i < len(word); i++ {
			next, ok := node.children[word[i]]
			if !ok {
				return nil
			}
			node = next
		}
		return node
	}
	out := []bool{}
	for _, op := range ops {
		parts := strings.Fields(op)
		kind, word := parts[0], parts[1]
		switch kind {
		case "insert":
			node := root
			for i := 0; i < len(word); i++ {
				next, ok := node.children[word[i]]
				if !ok {
					next = newTrieNode()
					node.children[word[i]] = next
				}
				node = next
			}
			node.end = true
		case "search":
			node := walk(word)
			out = append(out, node != nil && node.end)
		default:
			out = append(out, walk(word) != nil)
		}
	}
	return out
}

func main() {
	fmt.Println(runTrie([]string{"insert apple", "search apple", "search app", "starts app", "insert app", "search app"}))
}
