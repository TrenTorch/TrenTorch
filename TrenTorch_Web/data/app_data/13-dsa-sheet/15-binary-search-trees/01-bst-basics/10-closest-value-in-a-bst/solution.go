package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func closestValue(root *TreeNode, target int) int {
	best := root.Val
	node := root
	for node != nil {
		dNode := absInt(node.Val - target)
		dBest := absInt(best - target)
		if dNode < dBest || (dNode == dBest && node.Val < best) {
			best = node.Val
		}
		if target < node.Val {
			node = node.Left
		} else {
			node = node.Right
		}
	}
	return best
}

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	// Call it here and print the result to try it.
}
