package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func oddEvenList(head *ListNode) *ListNode {
	if head == nil {
		return head
	}
	odd := head
	even := head.Next
	evenHead := even
	for even != nil && even.Next != nil {
		odd.Next = even.Next
		odd = odd.Next
		even.Next = odd.Next
		even = even.Next
	}
	odd.Next = evenHead
	return head
}

func main() {
	// Call it here and print the result to try it.
}
