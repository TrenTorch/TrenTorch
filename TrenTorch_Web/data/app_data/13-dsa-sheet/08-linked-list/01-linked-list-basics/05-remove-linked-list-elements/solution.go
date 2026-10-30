package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func removeElements(head *ListNode, val int) *ListNode {
	dummy := &ListNode{Next: head}
	prev, cur := dummy, head
	for cur != nil {
		if cur.Val == val {
			prev.Next = cur.Next
		} else {
			prev = cur
		}
		cur = cur.Next
	}
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
