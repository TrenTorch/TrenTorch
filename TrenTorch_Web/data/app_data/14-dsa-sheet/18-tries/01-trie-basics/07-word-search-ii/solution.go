package main

import (
	"fmt"
	"sort"
)

type wsNode struct {
	children map[byte]*wsNode
	word     string
	hasWord  bool
}

func newWsNode() *wsNode {
	return &wsNode{children: map[byte]*wsNode{}}
}

// O(R * C * 4^L) time worst case (L = longest word), O(total word length) space
func findWords(board []string, words []string) []string {
	rows := len(board)
	cols := 0
	if rows > 0 {
		cols = len(board[0])
	}
	root := newWsNode()
	for _, w := range words {
		node := root
		for i := 0; i < len(w); i++ {
			next, ok := node.children[w[i]]
			if !ok {
				next = newWsNode()
				node.children[w[i]] = next
			}
			node = next
		}
		node.word = w
		node.hasWord = true
	}
	grid := make([][]byte, rows)
	for r := range board {
		grid[r] = []byte(board[r])
	}
	found := map[string]bool{}
	var dfs func(r, c int, node *wsNode)
	dfs = func(r, c int, node *wsNode) {
		ch := grid[r][c]
		nxt, ok := node.children[ch]
		if !ok {
			return
		}
		if nxt.hasWord {
			found[nxt.word] = true
		}
		grid[r][c] = '#'
		dirs := [4][2]int{{r + 1, c}, {r - 1, c}, {r, c + 1}, {r, c - 1}}
		for _, d := range dirs {
			nr, nc := d[0], d[1]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != '#' {
				dfs(nr, nc, nxt)
			}
		}
		grid[r][c] = ch
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			dfs(r, c, root)
		}
	}
	res := make([]string, 0, len(found))
	for w := range found {
		res = append(res, w)
	}
	sort.Strings(res)
	return res
}

func main() {
	fmt.Println(findWords([]string{"oaan", "etae", "ihkr", "iflv"}, []string{"oath", "pea", "eat", "rain"}))
}
