class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static ListNode rotateList(ListNode head, long k) {
        if (head == null || head.next == null) {
            return head;
        }
        long length = 1;
        ListNode tail = head;
        while (tail.next != null) {
            tail = tail.next;
            length++;
        }
        long shift = k % length;
        if (shift == 0) {
            return head;
        }
        ListNode newTail = head;
        for (long i = 0; i < length - shift - 1; i++) {
            newTail = newTail.next;
        }
        ListNode newHead = newTail.next;
        newTail.next = null;
        tail.next = head;
        return newHead;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
