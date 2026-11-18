class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static long cycleLength(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                long length = 1;
                ListNode node = slow.next;
                while (node != slow) {
                    node = node.next;
                    length++;
                }
                return length;
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
