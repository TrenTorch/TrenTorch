package main

import "fmt"

type ipNode struct {
	children map[byte]*ipNode
	end      bool
}

func newIpNode() *ipNode {
	return &ipNode{children: map[byte]*ipNode{}}
}

// O(N * L + T * L) time (N = text length, T = number of words, L = max word length), O(total word length) space
func indexPairs(text string, words []string) [][]int {
	root := newIpNode()
	for _, w := range words {
		node := root
		for i := 0; i < len(w); i++ {
			next, ok := node.children[w[i]]
			if !ok {
				next = newIpNode()
				node.children[w[i]] = next
			}
			node = next
		}
		node.end = true
	}
	out := [][]int{}
	for i := 0; i < len(text); i++ {
		node := root
		for j := i; j < len(text); j++ {
			next, ok := node.children[text[j]]
			if !ok {
				break
			}
			node = next
			if node.end {
				out = append(out, []int{i, j})
			}
		}
	}
	return out
}

func main() {
	fmt.Println(indexPairs("thestoryofleetcodeandme", []string{"story", "fleet", "leetcode"}))
}
