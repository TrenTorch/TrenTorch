package main

import "fmt"

type encNode struct {
	children map[byte]*encNode
}

func newEncNode() *encNode {
	return &encNode{children: map[byte]*encNode{}}
}

// O(total word length) time, O(total word length) space
func minimumLengthEncoding(words []string) int {
	type endInfo struct {
		node   *encNode
		length int
	}
	root := newEncNode()
	seen := map[string]bool{}
	ends := []endInfo{}
	for _, w := range words {
		if seen[w] {
			continue
		}
		seen[w] = true
		node := root
		for i := len(w) - 1; i >= 0; i-- {
			next, ok := node.children[w[i]]
			if !ok {
				next = newEncNode()
				node.children[w[i]] = next
			}
			node = next
		}
		ends = append(ends, endInfo{node: node, length: len(w)})
	}
	total := 0
	for _, e := range ends {
		if len(e.node.children) == 0 {
			total += e.length + 1
		}
	}
	return total
}

func main() {
	fmt.Println(minimumLengthEncoding([]string{"time", "me", "bell"}))
}
