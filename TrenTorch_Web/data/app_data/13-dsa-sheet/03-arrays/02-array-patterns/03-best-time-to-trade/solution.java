public class Main {
    // O(n) time, O(1) space
    static long stockBestProfit(long[] prices) {
        long best = 0;
        boolean hasLowest = false;
        long lowest = 0;
        for (long price : prices) {
            if (hasLowest) {
                best = Math.max(best, price - lowest);
                lowest = Math.min(lowest, price);
            } else {
                lowest = price;
                hasLowest = true;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(stockBestProfit(new long[]{7L, 1L, 5L, 3L, 6L, 4L}));
    }
}
