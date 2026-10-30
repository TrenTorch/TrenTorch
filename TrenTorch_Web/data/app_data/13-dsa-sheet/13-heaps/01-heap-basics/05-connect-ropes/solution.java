import java.util.PriorityQueue;

public class Main {
    // O(n log n) time, O(n) space
    static long connectRopes(long[] ropes) {
        PriorityQueue<Long> minHeap = new PriorityQueue<>();
        for (long rope : ropes) {
            minHeap.offer(rope);
        }
        long total = 0;
        while (minHeap.size() > 1) {
            long a = minHeap.poll();
            long b = minHeap.poll();
            long joined = a + b;
            total += joined;
            minHeap.offer(joined);
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(connectRopes(new long[]{4L, 3L, 2L, 6L}));
    }
}
