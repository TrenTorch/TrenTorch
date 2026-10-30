package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// merges two sorted lists in O(m + n) time, O(1) space
func mergeSortedLists(a, b *ListNode) *ListNode {
	dummy := &ListNode{}
	tail := dummy
	for a != nil && b != nil {
		if a.Val <= b.Val {
			tail.Next = a
			a = a.Next
		} else {
			tail.Next = b
			b = b.Next
		}
		tail = tail.Next
	}
	if a != nil {
		tail.Next = a
	} else {
		tail.Next = b
	}
	return dummy.Next
}

// O(n log n) time, O(log n) space (recursion stack)
func sortList(head *ListNode) *ListNode {
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
	return mergeSortedLists(sortList(head), sortList(second))
}

func main() {
	// Call it here and print the result to try it.
}
