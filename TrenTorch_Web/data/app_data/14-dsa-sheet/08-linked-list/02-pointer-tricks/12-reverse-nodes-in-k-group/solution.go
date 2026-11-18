package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func reverseKGroup(head *ListNode, k int) *ListNode {
	dummy := &ListNode{Val: 0, Next: head}
	groupPrev := dummy
	for {
		kth := groupPrev
		for i := 0; i < k; i++ {
			kth = kth.Next
			if kth == nil {
				return dummy.Next
			}
		}
		groupNext := kth.Next
		prev, cur := groupNext, groupPrev.Next
		for cur != groupNext {
			after := cur.Next
			cur.Next = prev
			prev = cur
			cur = after
		}
		first := groupPrev.Next
		groupPrev.Next = kth
		groupPrev = first
	}
}

func main() {
	// Call it here and print the result to try it.
}
