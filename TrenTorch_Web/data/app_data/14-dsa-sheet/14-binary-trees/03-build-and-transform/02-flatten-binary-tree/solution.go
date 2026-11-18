package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(1) extra space
func flattenTree(root *TreeNode) *TreeNode {
	node := root
	for node != nil {
		if node.Left != nil {
			tail := node.Left
			for tail.Right != nil {
				tail = tail.Right
			}
			tail.Right = node.Right
			node.Right = node.Left
			node.Left = nil
		}
		node = node.Right
	}
	return root
}

func main() {
	// Call it here and print the result to try it.
}
