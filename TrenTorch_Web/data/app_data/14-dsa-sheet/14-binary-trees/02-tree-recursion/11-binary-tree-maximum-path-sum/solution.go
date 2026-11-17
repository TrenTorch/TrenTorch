package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func maxPathSum(root *TreeNode) int {
	best := root.Val
	var gain func(node *TreeNode) int
	gain = func(node *TreeNode) int {
		if node == nil {
			return 0
		}
		left := max(0, gain(node.Left))
		right := max(0, gain(node.Right))
		best = max(best, node.Val+left+right)
		return node.Val + max(left, right)
	}
	gain(root)
	return best
}

func main() {
	// Call it here and print the result to try it.
}
