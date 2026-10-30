package main

import (
	"fmt"
	"strings"
)

type rootNode struct {
	children map[byte]*rootNode
	end      bool
}

func newRootNode() *rootNode {
	return &rootNode{children: map[byte]*rootNode{}}
}

// O(total root length + sentence length) time, O(total root length) space
func replaceWords(roots []string, sentence string) string {
	root := newRootNode()
	for _, r := range roots {
		node := root
		for i := 0; i < len(r); i++ {
			next, ok := node.children[r[i]]
			if !ok {
				next = newRootNode()
				node.children[r[i]] = next
			}
			node = next
		}
		node.end = true
	}
	out := []string{}
	for _, word := range strings.Fields(sentence) {
		node := root
		replaced := false
		for i := 0; i < len(word); i++ {
			next, ok := node.children[word[i]]
			if !ok {
				break
			}
			node = next
			if node.end {
				out = append(out, word[:i+1])
				replaced = true
				break
			}
		}
		if !replaced {
			out = append(out, word)
		}
	}
	return strings.Join(out, " ")
}

func main() {
	fmt.Println(replaceWords([]string{"cat", "bat", "rat"}, "the cattle was rattled by the battery"))
}
