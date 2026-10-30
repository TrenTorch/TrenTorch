public class Main {
    // O(n log n) time, O(n) space
    static boolean isNStraightHand(long[] hand, long groupSize) {
        if (hand.length % groupSize != 0) {
            return false;
        }
        java.util.Map<Long, Integer> count = new java.util.HashMap<>();
        for (long x : hand) {
            count.merge(x, 1, Integer::sum);
        }
        java.util.PriorityQueue<Long> heap = new java.util.PriorityQueue<>(count.keySet());
        while (!heap.isEmpty()) {
            long start = heap.peek();
            for (long x = start; x < start + groupSize; x++) {
                int c = count.getOrDefault(x, 0);
                if (c == 0) {
                    return false;
                }
                count.put(x, c - 1);
                if (c - 1 == 0) {
                    if (x != heap.peek()) {
                        return false;
                    }
                    heap.poll();
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isNStraightHand(new long[]{1L, 2L, 3L, 6L, 2L, 3L, 4L, 7L, 8L}, 3L));
    }
}
