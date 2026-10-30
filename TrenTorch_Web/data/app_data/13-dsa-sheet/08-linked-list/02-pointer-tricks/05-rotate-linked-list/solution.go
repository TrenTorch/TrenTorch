package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func rotateList(head *ListNode, k int) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}
	length := 1
	tail := head
	for tail.Next != nil {
		tail = tail.Next
		length++
	}
	k %= length
	if k == 0 {
		return head
	}
	newTail := head
	for i := 0; i < length-k-1; i++ {
		newTail = newTail.Next
	}
	newHead := newTail.Next
	newTail.Next = nil
	tail.Next = head
	return newHead
}

func main() {
	// Call it here and print the result to try it.
}
