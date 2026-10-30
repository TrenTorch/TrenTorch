import java.util.Arrays;

public class Main {
    // O(2^n * n^2) time, O(2^n * n) space
    static long tsp(long[][] dist) {
        int n = dist.length;
        if (n <= 1) {
            return 0;
        }
        final long INF = Long.MAX_VALUE;
        int full = (1 << n) - 1;
        long[][] best = new long[1 << n][n];
        for (long[] row : best) {
            Arrays.fill(row, INF);
        }
        best[1][0] = 0;
        for (int mask = 1; mask <= full; mask++) {
            if ((mask & 1) == 0) {
                continue;
            }
            for (int last = 0; last < n; last++) {
                long cost = best[mask][last];
                if (cost == INF) {
                    continue;
                }
                for (int nxt = 0; nxt < n; nxt++) {
                    if (((mask >> nxt) & 1) == 0) {
                        int newMask = mask | (1 << nxt);
                        long value = cost + dist[last][nxt];
                        if (value < best[newMask][nxt]) {
                            best[newMask][nxt] = value;
                        }
                    }
                }
            }
        }
        long result = INF;
        for (int last = 1; last < n; last++) {
            if (best[full][last] == INF) {
                continue;
            }
            result = Math.min(result, best[full][last] + dist[last][0]);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(tsp(new long[][]{new long[]{0L, 10L, 15L, 20L}, new long[]{10L, 0L, 35L, 25L}, new long[]{15L, 35L, 0L, 30L}, new long[]{20L, 25L, 30L, 0L}}));
    }
}
