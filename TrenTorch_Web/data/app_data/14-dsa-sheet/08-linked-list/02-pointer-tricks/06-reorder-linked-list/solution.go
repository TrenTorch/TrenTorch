package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func reorderList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}
	slow, fast := head, head.Next
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}
	second := slow.Next
	slow.Next = nil
	var prev *ListNode
	for second != nil {
		after := second.Next
		second.Next = prev
		prev = second
		second = after
	}
	first := head
	second = prev
	for second != nil {
		a, b := first.Next, second.Next
		first.Next = second
		second.Next = a
		first, second = a, b
	}
	return head
}

func main() {
	// Call it here and print the result to try it.
}
