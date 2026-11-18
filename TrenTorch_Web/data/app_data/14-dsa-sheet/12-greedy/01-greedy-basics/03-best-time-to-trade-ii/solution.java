public class Main {
    // O(n) time, O(1) space
    static long maxProfitMany(long[] prices) {
        long profit = 0;
        for (int i = 1; i < prices.length; i++) {
            long diff = prices[i] - prices[i - 1];
            if (diff > 0) profit += diff;
        }
        return profit;
    }

    public static void main(String[] args) {
        System.out.println(maxProfitMany(new long[]{7L, 1L, 5L, 3L, 6L, 4L}));
    }
}
