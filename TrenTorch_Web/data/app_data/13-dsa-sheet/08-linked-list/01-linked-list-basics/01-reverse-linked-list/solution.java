class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        while (head != null) {
            ListNode after = head.next;
            head.next = prev;
            prev = head;
            head = after;
        }
        return prev;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
