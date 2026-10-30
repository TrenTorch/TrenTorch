class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static ListNode reorderList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode second = slow.next;
        slow.next = null;
        ListNode prev = null;
        while (second != null) {
            ListNode after = second.next;
            second.next = prev;
            prev = second;
            second = after;
        }
        ListNode first = head;
        second = prev;
        while (second != null) {
            ListNode a = first.next;
            ListNode b = second.next;
            first.next = second;
            second.next = a;
            first = a;
            second = b;
        }
        return head;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
