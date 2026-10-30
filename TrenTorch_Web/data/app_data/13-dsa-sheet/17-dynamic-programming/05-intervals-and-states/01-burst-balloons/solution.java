public class Main {
    // O(n^3) time, O(n^2) space
    static long maxCoins(long[] nums) {
        int n = nums.length;
        long[] a = new long[n + 2];
        a[0] = 1;
        a[n + 1] = 1;
        for (int i = 0; i < n; i++) {
            a[i + 1] = nums[i];
        }
        int m = n + 2;
        long[][] dp = new long[m][m];
        for (int length = 2; length < m; length++) {
            for (int i = 0; i + length < m; i++) {
                int j = i + length;
                long best = 0;
                for (int k = i + 1; k < j; k++) {
                    long value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j];
                    if (value > best) {
                        best = value;
                    }
                }
                dp[i][j] = best;
            }
        }
        return dp[0][m - 1];
    }

    public static void main(String[] args) {
        System.out.println(maxCoins(new long[]{3L, 1L, 5L, 8L}));
    }
}
