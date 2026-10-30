public class Main {
    // O(n log n) time, O(n) space
    static long lastStoneWeight(long[] stones) {
        java.util.PriorityQueue<Long> heap = new java.util.PriorityQueue<>(java.util.Collections.reverseOrder());
        for (long s : stones) {
            heap.add(s);
        }
        while (heap.size() > 1) {
            long a = heap.poll();
            long b = heap.poll();
            if (a != b) {
                heap.add(a - b);
            }
        }
        if (heap.isEmpty()) {
            return 0;
        }
        return heap.peek();
    }

    public static void main(String[] args) {
        System.out.println(lastStoneWeight(new long[]{2L, 7L, 4L, 1L, 8L, 1L}));
    }
}
