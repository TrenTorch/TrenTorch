public class Main {
    // Definition for singly-linked list.
    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int x) {
            val = x;
            next = null;
        }
    }

    // O(m+n) time, O(1) space
    public static ListNode intersectionNode(ListNode listA, ListNode listB) {
        ListNode pa = listA;
        ListNode pb = listB;
        while (pa != pb) {
            pa = (pa != null) ? pa.next : listB;
            pb = (pb != null) ? pb.next : listA;
        }
        return pa;
    }

    public static void main(String[] args) {
    }
}
