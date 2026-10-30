public class Main {
    // O(n * capacity) time, O(capacity) space
    static long unboundedKnapsack(long[] weights, long[] values, long capacity) {
        int cap = (int) capacity;
        long[] dp = new long[cap + 1];
        for (int i = 0; i < weights.length; i++) {
            int w = (int) weights[i];
            long v = values[i];
            for (int j = w; j <= cap; j++) {
                long candidate = dp[j - w] + v;
                if (candidate > dp[j]) {
                    dp[j] = candidate;
                }
            }
        }
        return dp[cap];
    }

    public static void main(String[] args) {
        System.out.println(unboundedKnapsack(new long[]{1L, 3L, 4L}, new long[]{15L, 50L, 60L}, 8L));
    }
}
