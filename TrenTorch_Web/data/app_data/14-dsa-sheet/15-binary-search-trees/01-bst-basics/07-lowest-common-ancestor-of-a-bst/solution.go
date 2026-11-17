package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func lcaBst(root *TreeNode, p int, q int) *TreeNode {
	node := root
	for node != nil {
		if p < node.Val && q < node.Val {
			node = node.Left
		} else if p > node.Val && q > node.Val {
			node = node.Right
		} else {
			return node
		}
	}
	return nil
}

func main() {
}
