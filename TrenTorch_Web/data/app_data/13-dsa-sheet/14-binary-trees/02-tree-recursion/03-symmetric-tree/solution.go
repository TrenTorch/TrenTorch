package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func isSymmetric(root *TreeNode) bool {
	var mirror func(a, b *TreeNode) bool
	mirror = func(a, b *TreeNode) bool {
		if a == nil && b == nil {
			return true
		}
		if a == nil || b == nil || a.Val != b.Val {
			return false
		}
		return mirror(a.Left, b.Right) && mirror(a.Right, b.Left)
	}
	return root == nil || mirror(root.Left, root.Right)
}

func main() {
	// Call it here and print the result to try it.
}
