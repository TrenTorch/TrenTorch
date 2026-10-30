class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static boolean isPalindromeList(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode prev = null;
        while (slow != null) {
            ListNode after = slow.next;
            slow.next = prev;
            prev = slow;
            slow = after;
        }
        ListNode left = head;
        ListNode right = prev;
        while (right != null) {
            if (left.val != right.val) {
                return false;
            }
            left = left.next;
            right = right.next;
        }
        return true;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
