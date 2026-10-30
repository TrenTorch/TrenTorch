public class Main {
    // O(dice * target) time, O(target) space
    static long diceWays(long dice, long faces, long target) {
        final int MOD = 1000000007;
        int t = (int) target;
        int f = (int) faces;
        int d = (int) dice;
        long[] row = new long[t + 1];
        row[0] = 1;
        for (int i = 0; i < d; i++) {
            long[] prefix = new long[t + 2];
            for (int j = 0; j <= t; j++) {
                prefix[j + 1] = (prefix[j] + row[j]) % MOD;
            }
            long[] nxt = new long[t + 1];
            for (int j = 1; j <= t; j++) {
                int left = Math.max(0, j - f);
                long val = (prefix[j] - prefix[left]) % MOD;
                if (val < 0) val += MOD;
                nxt[j] = val;
            }
            row = nxt;
        }
        return row[t];
    }

    public static void main(String[] args) {
        System.out.println(diceWays(2L, 6L, 7L));
    }
}
