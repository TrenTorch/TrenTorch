package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func isBalanced(root *TreeNode) bool {
	var check func(node *TreeNode) int
	check = func(node *TreeNode) int {
		if node == nil {
			return 0
		}
		left := check(node.Left)
		if left == -1 {
			return -1
		}
		right := check(node.Right)
		diff := left - right
		if diff < 0 {
			diff = -diff
		}
		if right == -1 || diff > 1 {
			return -1
		}
		return 1 + max(left, right)
	}
	return check(root) != -1
}

func main() {
	// Call it here and print the result to try it.
}
