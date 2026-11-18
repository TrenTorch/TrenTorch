package main

import "fmt"

type prefixNode struct {
	children map[byte]*prefixNode
	count    int
}

func newPrefixNode() *prefixNode {
	return &prefixNode{children: map[byte]*prefixNode{}}
}

// O(total word length + total query length) time, O(total word length) space
func countWithPrefix(words []string, queries []string) []int {
	root := newPrefixNode()
	for _, word := range words {
		node := root
		for i := 0; i < len(word); i++ {
			child, ok := node.children[word[i]]
			if !ok {
				child = newPrefixNode()
				node.children[word[i]] = child
			}
			child.count++
			node = child
		}
	}
	out := make([]int, 0, len(queries))
	for _, q := range queries {
		node := root
		for i := 0; i < len(q); i++ {
			next, ok := node.children[q[i]]
			if !ok {
				node = nil
				break
			}
			node = next
		}
		if node != nil {
			out = append(out, node.count)
		} else {
			out = append(out, 0)
		}
	}
	return out
}

func main() {
	fmt.Println(countWithPrefix([]string{"apple", "app", "apt", "bat"}, []string{"ap", "app", "b", "c"}))
}
