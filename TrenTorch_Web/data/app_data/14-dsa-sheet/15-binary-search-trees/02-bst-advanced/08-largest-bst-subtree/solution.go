package main

import "math"

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space (h = tree height, used by the recursion)
func largestBstSubtree(root *TreeNode) int {
	best := 0
	var walk func(node *TreeNode) (int, int, int)
	walk = func(node *TreeNode) (int, int, int) {
		if node == nil {
			return 0, math.MaxInt, math.MinInt
		}
		leftSize, leftLow, leftHigh := walk(node.Left)
		rightSize, rightLow, rightHigh := walk(node.Right)
		if leftSize >= 0 && rightSize >= 0 && leftHigh < node.Val && node.Val < rightLow {
			size := leftSize + rightSize + 1
			if size > best {
				best = size
			}
			return size, min(leftLow, node.Val), max(rightHigh, node.Val)
		}
		return -1, math.MinInt, math.MaxInt
	}
	walk(root)
	return best
}

func main() {
	// Call it here and print the result to try it.
}
