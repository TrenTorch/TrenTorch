package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func searchBst(root *TreeNode, val int) *TreeNode {
	node := root
	for node != nil && node.Val != val {
		if val < node.Val {
			node = node.Left
		} else {
			node = node.Right
		}
	}
	return node
}

func main() {
	// Call it here and print the result to try it.
}
