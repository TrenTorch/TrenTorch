public class Main {
    // O(n * capacity) time, O(capacity) space
    static long knapsack(long[] weights, long[] values, long capacity) {
        int cap = (int) capacity;
        long[] best = new long[cap + 1];
        for (int i = 0; i < weights.length; i++) {
            long weight = weights[i];
            long value = values[i];
            for (int w = cap; w >= weight; w--) {
                long candidate = best[w - (int) weight] + value;
                if (candidate > best[w]) {
                    best[w] = candidate;
                }
            }
        }
        return best[cap];
    }

    public static void main(String[] args) {
        System.out.println(knapsack(new long[]{1L, 3L, 4L, 5L}, new long[]{1L, 4L, 5L, 7L}, 7L));
    }
}
