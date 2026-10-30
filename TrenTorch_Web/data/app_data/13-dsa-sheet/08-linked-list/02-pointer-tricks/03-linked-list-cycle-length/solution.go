package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func cycleLength(head *ListNode) int {
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
		if slow == fast {
			length := 1
			node := slow.Next
			for node != slow {
				node = node.Next
				length++
			}
			return length
		}
	}
	return 0
}

func main() {
	// Call it here and print the result to try it.
}
