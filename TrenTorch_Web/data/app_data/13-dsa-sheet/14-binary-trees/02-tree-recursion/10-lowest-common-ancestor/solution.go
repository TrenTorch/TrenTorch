package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func lowestCommonAncestor(root *TreeNode, p, q int) *TreeNode {
	if root == nil || root.Val == p || root.Val == q {
		return root
	}
	left := lowestCommonAncestor(root.Left, p, q)
	right := lowestCommonAncestor(root.Right, p, q)
	if left != nil && right != nil {
		return root
	}
	if left != nil {
		return left
	}
	return right
}

func main() {
}
