import java.util.Arrays;

public class Main {
    // O(n*k) time, O(k) space
    static long maxProfitK(long k, long[] prices) {
        if (k == 0 || prices.length < 2) {
            return 0;
        }
        if (k >= prices.length / 2) {
            long profit = 0;
            for (int i = 1; i < prices.length; i++) {
                long diff = prices[i] - prices[i - 1];
                if (diff > 0) profit += diff;
            }
            return profit;
        }
        int K = (int) k;
        long[] hold = new long[K + 1];
        long[] free = new long[K + 1];
        Arrays.fill(hold, Long.MIN_VALUE);
        Arrays.fill(free, 0);
        for (long p : prices) {
            for (int t = 1; t <= K; t++) {
                hold[t] = Math.max(hold[t], free[t - 1] - p);
                free[t] = Math.max(free[t], hold[t] + p);
            }
        }
        return free[K];
    }

    public static void main(String[] args) {
        System.out.println(maxProfitK(2L, new long[]{3L, 2L, 6L, 5L, 0L, 3L}));
    }
}
