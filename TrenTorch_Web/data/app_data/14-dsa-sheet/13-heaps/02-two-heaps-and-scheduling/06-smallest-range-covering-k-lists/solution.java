import java.util.PriorityQueue;
import java.util.Arrays;

public class Main {
    // O(N log k) time, O(k) space where N is total number of elements
    static long[] smallestRange(long[][] lists) {
        record Node(long value, int listIdx, int elemIdx) {}
        PriorityQueue<Node> heap = new PriorityQueue<>((a, b) -> Long.compare(a.value, b.value));
        long currentMax = Long.MIN_VALUE;
        for (int i = 0; i < lists.length; i++) {
            long val = lists[i][0];
            heap.add(new Node(val, i, 0));
            if (val > currentMax) currentMax = val;
        }
        long[] best = new long[]{heap.peek().value, currentMax};
        while (true) {
            Node node = heap.poll();
            long value = node.value;
            int i = node.listIdx;
            int j = node.elemIdx;
            if (currentMax - value < best[1] - best[0] || (currentMax - value == best[1] - best[0] && value < best[0])) {
                best[0] = value;
                best[1] = currentMax;
            }
            if (j + 1 == lists[i].length) {
                return best;
            }
            long nextVal = lists[i][j + 1];
            if (nextVal > currentMax) currentMax = nextVal;
            heap.add(new Node(nextVal, i, j + 1));
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(smallestRange(new long[][]{new long[]{4L, 10L, 15L, 24L, 26L}, new long[]{0L, 9L, 12L, 20L}, new long[]{5L, 18L, 22L, 30L}})));
    }
}
