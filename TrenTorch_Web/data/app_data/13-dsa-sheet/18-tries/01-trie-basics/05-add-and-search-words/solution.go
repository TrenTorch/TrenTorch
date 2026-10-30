package main

import (
	"fmt"
	"strings"
)

type wdNode struct {
	children map[byte]*wdNode
	end      bool
}

func newWdNode() *wdNode {
	return &wdNode{children: map[byte]*wdNode{}}
}

// wdSearch matches text[i:] against the trie below node, where '.' matches any letter.
func wdSearch(node *wdNode, text string, i int) bool {
	if i == len(text) {
		return node.end
	}
	ch := text[i]
	if ch == '.' {
		for _, child := range node.children {
			if wdSearch(child, text, i+1) {
				return true
			}
		}
		return false
	}
	child, ok := node.children[ch]
	return ok && wdSearch(child, text, i+1)
}

// O(L) time per add, O(26^L) worst case per search (L = word length), O(total added length) space
func runWordDictionary(ops []string) []bool {
	root := newWdNode()
	out := []bool{}
	for _, op := range ops {
		parts := strings.Fields(op)
		kind, text := parts[0], parts[1]
		if kind == "add" {
			node := root
			for i := 0; i < len(text); i++ {
				next, ok := node.children[text[i]]
				if !ok {
					next = newWdNode()
					node.children[text[i]] = next
				}
				node = next
			}
			node.end = true
		} else {
			out = append(out, wdSearch(root, text, 0))
		}
	}
	return out
}

func main() {
	fmt.Println(runWordDictionary([]string{"add bad", "add dad", "add mad", "search pad", "search bad", "search .ad", "search b.."}))
}
