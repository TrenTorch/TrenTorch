package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// inorderValues returns the values of a BST in increasing order.
func inorderValues(root *TreeNode) []int {
	out := []int{}
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		out = append(out, node.Val)
		node = node.Right
	}
	return out
}

// O(n + m) time, O(n + m) space for the two sorted lists and the merged output
func mergeBsts(root1 *TreeNode, root2 *TreeNode) []int {
	a, b := inorderValues(root1), inorderValues(root2)
	out := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			out = append(out, a[i])
			i++
		} else {
			out = append(out, b[j])
			j++
		}
	}
	out = append(out, a[i:]...)
	out = append(out, b[j:]...)
	return out
}

func main() {
	// Call it here and print the result to try it.
}
