public class Main {
    // O(n^2) time, O(n^2) space where n = cuts.length + 2
    static long minCostCut(long length, long[] cuts) {
        // Sort cuts and build points array with boundaries
        java.util.Arrays.sort(cuts);
        int m = cuts.length;
        long[] points = new long[m + 2];
        points[0] = 0;
        for (int i = 0; i < m; i++) {
            points[i + 1] = cuts[i];
        }
        points[m + 1] = length;
        int n = m + 2;

        long[][] dp = new long[n][n];
        int[][] bestCut = new int[n][n];

        // Base case: intervals of length 1 (no cuts inside) have cost 0
        for (int i = 0; i < n - 1; i++) {
            bestCut[i][i + 1] = i + 1;
        }

        // DP over increasing span
        for (int span = 2; span < n; span++) {
            for (int i = 0; i + span < n; i++) {
                int j = i + span;
                int low = Math.max(i + 1, bestCut[i][j - 1]);
                int high = Math.min(j - 1, bestCut[i + 1][j]);
                long best = Long.MAX_VALUE;
                int bestK = -1;
                for (int k = low; k <= high; k++) {
                    long value = dp[i][k] + dp[k][j];
                    if (value < best) {
                        best = value;
                        bestK = k;
                    }
                }
                dp[i][j] = best + points[j] - points[i];
                bestCut[i][j] = bestK;
            }
        }
        return dp[0][n - 1];
    }

    public static void main(String[] args) {
        System.out.println(minCostCut(7L, new long[]{1L, 3L, 4L, 5L}));
    }
}
