class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static ListNode partitionList(ListNode head, long x) {
        ListNode smallDummy = new ListNode(0);
        ListNode largeDummy = new ListNode(0);
        ListNode smallTail = smallDummy;
        ListNode largeTail = largeDummy;
        while (head != null) {
            if (head.val < x) {
                smallTail.next = head;
                smallTail = head;
            } else {
                largeTail.next = head;
                largeTail = head;
            }
            head = head.next;
        }
        largeTail.next = null;
        smallTail.next = largeDummy.next;
        return smallDummy.next;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
