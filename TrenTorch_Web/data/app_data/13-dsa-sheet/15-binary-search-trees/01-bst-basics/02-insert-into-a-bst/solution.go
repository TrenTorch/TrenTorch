package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func insertIntoBst(root *TreeNode, val int) *TreeNode {
	if root == nil {
		return &TreeNode{Val: val}
	}
	node := root
	for {
		if val < node.Val {
			if node.Left == nil {
				node.Left = &TreeNode{Val: val}
				break
			}
			node = node.Left
		} else {
			if node.Right == nil {
				node.Right = &TreeNode{Val: val}
				break
			}
			node = node.Right
		}
	}
	return root
}

func main() {
	// Call it here and print the result to try it.
}
