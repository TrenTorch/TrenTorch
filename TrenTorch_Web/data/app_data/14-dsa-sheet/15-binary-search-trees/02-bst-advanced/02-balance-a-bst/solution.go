package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(n) space for the sorted values and the new tree
func balanceBst(root *TreeNode) *TreeNode {
	values := []int{}
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		values = append(values, node.Val)
		node = node.Right
	}

	var build func(lo, hi int) *TreeNode
	build = func(lo, hi int) *TreeNode {
		if lo > hi {
			return nil
		}
		mid := (lo + hi) / 2
		return &TreeNode{Val: values[mid], Left: build(lo, mid-1), Right: build(mid+1, hi)}
	}
	return build(0, len(values)-1)
}

func main() {
	// Call it here and print the result to try it.
}
