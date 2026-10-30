class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(max(M, N)) time, O(max(M, N)) space for the result list
    static ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        long carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            long total = carry;
            if (l1 != null) {
                total += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                total += l2.val;
                l2 = l2.next;
            }
            tail.next = new ListNode(total % 10);
            tail = tail.next;
            carry = total / 10;
        }
        return dummy.next;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
