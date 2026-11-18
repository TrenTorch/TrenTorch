public class Main {
    // O(amount * len(coins)) time, O(amount) space
    static long coinChange(long[] coins, long amount) {
        if (amount == 0) return 0;
        int n = (int) amount;
        long[] best = new long[n + 1];
        long INF = n + 1L;
        best[0] = 0;
        for (int i = 1; i <= n; i++) {
            best[i] = INF;
        }
        for (int a = 1; a <= n; a++) {
            for (long c : coins) {
                if (c <= a) {
                    long candidate = best[a - (int)c] + 1;
                    if (candidate < best[a]) {
                        best[a] = candidate;
                    }
                }
            }
        }
        return best[n] != INF ? best[n] : -1;
    }

    public static void main(String[] args) {
        System.out.println(coinChange(new long[]{1L, 2L, 5L}, 11L));
    }
}
