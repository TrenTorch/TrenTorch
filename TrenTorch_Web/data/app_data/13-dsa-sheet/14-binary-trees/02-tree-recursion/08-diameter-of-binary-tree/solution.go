package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func diameter(root *TreeNode) int {
	best := 0
	var height func(node *TreeNode) int
	height = func(node *TreeNode) int {
		if node == nil {
			return 0
		}
		left := height(node.Left)
		right := height(node.Right)
		best = max(best, left+right)
		return 1 + max(left, right)
	}
	height(root)
	return best
}

func main() {
	// Call it here and print the result to try it.
}
