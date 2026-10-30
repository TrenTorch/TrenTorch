import java.util.*;

class ListNode {
    long val;
    ListNode next;
    ListNode(long val) { this.val = val; }
}

public class Main {
    private static class Entry {
        final long val;
        final int idx;
        final ListNode node;

        Entry(long val, int idx, ListNode node) {
            this.val = val;
            this.idx = idx;
            this.node = node;
        }
    }

    // O(N log k) time for N total nodes and k lists, O(k) space for the heap
    static ListNode mergeKLists(List<ListNode> lists) {
        PriorityQueue<Entry> heap = new PriorityQueue<>(
                Comparator.<Entry>comparingLong(e -> e.val).thenComparingInt(e -> e.idx));
        for (int i = 0; i < lists.size(); i++) {
            ListNode node = lists.get(i);
            if (node != null) {
                heap.add(new Entry(node.val, i, node));
            }
        }
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!heap.isEmpty()) {
            Entry e = heap.poll();
            tail.next = e.node;
            tail = e.node;
            if (e.node.next != null) {
                heap.add(new Entry(e.node.next.val, e.idx, e.node.next));
            }
        }
        return dummy.next;
    }

    public static void main(String[] args) {
    }
}
