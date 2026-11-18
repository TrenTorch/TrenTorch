public class Main {
    // O(n^3) time, O(n^2) space
    static long matrixChainCost(long[] dims) {
        int n = dims.length;
        if (n < 3) {
            return 0;
        }
        long[][] dp = new long[n][n];
        for (int length = 2; length < n; length++) {
            for (int i = 0; i < n - length; i++) {
                int j = i + length;
                long best = Long.MAX_VALUE;
                for (int k = i + 1; k < j; k++) {
                    long value = dp[i][k] + dp[k][j] + dims[i] * dims[k] * dims[j];
                    if (value < best) {
                        best = value;
                    }
                }
                dp[i][j] = best;
            }
        }
        return dp[0][n - 1];
    }

    public static void main(String[] args) {
        System.out.println(matrixChainCost(new long[]{10L, 30L, 5L, 60L}));
    }
}
