package main

import "sort"

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

type colEntry struct {
	row, val int
}

type colItem struct {
	node     *TreeNode
	row, col int
}

// O(n log n) time, O(n) space
func verticalOrder(root *TreeNode) [][]int {
	out := [][]int{}
	if root == nil {
		return out
	}
	columns := map[int][]colEntry{}
	queue := []colItem{{root, 0, 0}}
	for i := 0; i < len(queue); i++ {
		it := queue[i]
		columns[it.col] = append(columns[it.col], colEntry{it.row, it.node.Val})
		if it.node.Left != nil {
			queue = append(queue, colItem{it.node.Left, it.row + 1, it.col - 1})
		}
		if it.node.Right != nil {
			queue = append(queue, colItem{it.node.Right, it.row + 1, it.col + 1})
		}
	}
	cols := make([]int, 0, len(columns))
	for c := range columns {
		cols = append(cols, c)
	}
	sort.Ints(cols)
	for _, c := range cols {
		entries := columns[c]
		sort.Slice(entries, func(i, j int) bool {
			if entries[i].row != entries[j].row {
				return entries[i].row < entries[j].row
			}
			return entries[i].val < entries[j].val
		})
		vals := make([]int, len(entries))
		for i, e := range entries {
			vals[i] = e.val
		}
		out = append(out, vals)
	}
	return out
}

func main() {
	// Call it here and print the result to try it.
}
