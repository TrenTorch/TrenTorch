class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static ListNode reverseKGroup(ListNode head, long k) {
        if (head == null || k == 1) return head;
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode groupPrev = dummy;
        int kInt = (int) k;
        while (true) {
            ListNode kth = groupPrev;
            for (int i = 0; i < kInt; i++) {
                kth = kth.next;
                if (kth == null) {
                    return dummy.next;
                }
            }
            ListNode groupNext = kth.next;
            ListNode prev = groupNext;
            ListNode cur = groupPrev.next;
            while (cur != groupNext) {
                ListNode after = cur.next;
                cur.next = prev;
                prev = cur;
                cur = after;
            }
            ListNode first = groupPrev.next;
            groupPrev.next = kth;
            groupPrev = first;
        }
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
