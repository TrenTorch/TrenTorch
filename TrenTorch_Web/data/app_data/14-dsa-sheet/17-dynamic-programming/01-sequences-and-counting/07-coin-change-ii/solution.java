public class Main {
    // O(len(coins) * amount) time, O(amount) space
    static long countChange(long amount, long[] coins) {
        final long mod = 1_000_000_007L;
        int target = (int) amount;
        long[] ways = new long[target + 1];
        ways[0] = 1;
        for (long coin : coins) {
            int c = (int) coin;
            for (int a = c; a <= target; a++) {
                ways[a] = (ways[a] + ways[a - c]) % mod;
            }
        }
        return ways[target];
    }

    public static void main(String[] args) {
        System.out.println(countChange(5L, new long[]{1L, 2L, 5L}));
    }
}
