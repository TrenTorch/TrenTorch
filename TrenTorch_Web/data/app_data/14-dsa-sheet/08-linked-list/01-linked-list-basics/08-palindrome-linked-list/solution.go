package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) extra space (reverses the second half in place)
func isPalindromeList(head *ListNode) bool {
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}
	var prev *ListNode
	for slow != nil {
		after := slow.Next
		slow.Next = prev
		prev = slow
		slow = after
	}
	left, right := head, prev
	for right != nil {
		if left.Val != right.Val {
			return false
		}
		left = left.Next
		right = right.Next
	}
	return true
}

func main() {
	// Call it here and print the result to try it.
}
