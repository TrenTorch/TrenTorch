public class Main {
    // O(length^2) time, O(length) space
    static long rodCutting(long[] prices, long length) {
        int n = (int) length;
        long[] best = new long[n + 1];
        for (int len = 1; len <= n; len++) {
            for (int k = 1; k <= len; k++) {
                long candidate = prices[k - 1] + best[len - k];
                if (candidate > best[len]) {
                    best[len] = candidate;
                }
            }
        }
        return best[n];
    }

    public static void main(String[] args) {
        System.out.println(rodCutting(new long[]{1L, 5L, 8L, 9L, 10L, 17L, 17L, 20L}, 8L));
    }
}
