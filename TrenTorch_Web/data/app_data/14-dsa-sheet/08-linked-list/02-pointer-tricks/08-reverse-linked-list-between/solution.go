package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func reverseBetween(head *ListNode, left int, size int) *ListNode {
	dummy := &ListNode{Val: 0, Next: head}
	prev := dummy
	for i := 0; i < left-1; i++ {
		prev = prev.Next
	}
	cur := prev.Next
	for i := 0; i < size-1; i++ {
		nxt := cur.Next
		cur.Next = nxt.Next
		nxt.Next = prev.Next
		prev.Next = nxt
	}
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
