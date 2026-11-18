package main

import (
	"strconv"
	"strings"
)

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n * h) time, O(n * h) space
func rootToLeafPaths(root *TreeNode) []string {
	out := []string{}
	path := []string{}
	var walk func(node *TreeNode)
	walk = func(node *TreeNode) {
		if node == nil {
			return
		}
		path = append(path, strconv.Itoa(node.Val))
		if node.Left == nil && node.Right == nil {
			out = append(out, strings.Join(path, "->"))
		} else {
			walk(node.Left)
			walk(node.Right)
		}
		path = path[:len(path)-1]
	}
	walk(root)
	return out
}

func main() {
	// Call it here and print the result to try it.
}
