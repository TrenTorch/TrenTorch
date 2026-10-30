package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// treeIter yields the values of a BST in ascending order (forward)
// or descending order (backward), one at a time.
type treeIter struct {
	stack   []*TreeNode
	node    *TreeNode
	forward bool
}

func (it *treeIter) next() (int, bool) {
	for it.node != nil {
		it.stack = append(it.stack, it.node)
		if it.forward {
			it.node = it.node.Left
		} else {
			it.node = it.node.Right
		}
	}
	if len(it.stack) == 0 {
		return 0, false
	}
	n := it.stack[len(it.stack)-1]
	it.stack = it.stack[:len(it.stack)-1]
	if it.forward {
		it.node = n.Right
	} else {
		it.node = n.Left
	}
	return n.Val, true
}

// O(n) time, O(h) space where h is the tree height
func findTarget(root *TreeNode, k int) bool {
	up := &treeIter{node: root, forward: true}
	down := &treeIter{node: root, forward: false}
	lo, okLo := up.next()
	hi, okHi := down.next()
	for okLo && okHi && lo < hi {
		total := lo + hi
		if total == k {
			return true
		}
		if total < k {
			lo, okLo = up.next()
		} else {
			hi, okHi = down.next()
		}
	}
	return false
}

func main() {
	// Call it here and print the result to try it.
}
