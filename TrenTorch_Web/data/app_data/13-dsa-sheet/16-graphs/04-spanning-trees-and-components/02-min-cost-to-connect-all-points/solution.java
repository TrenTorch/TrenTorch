public class Main {
    // O(n^2) time, O(n) space
    static long minCostConnectPoints(long[][] points) {
        int n = points.length;
        if (n == 0) {
            return 0;
        }
        long[] best = new long[n];
        for (int i = 0; i < n; i++) {
            best[i] = Long.MAX_VALUE;
        }
        best[0] = 0;
        boolean[] used = new boolean[n];
        long total = 0;
        for (int i = 0; i < n; i++) {
            int u = -1;
            for (int v = 0; v < n; v++) {
                if (!used[v] && (u == -1 || best[v] < best[u])) {
                    u = v;
                }
            }
            used[u] = true;
            total += best[u];
            long ux = points[u][0];
            long uy = points[u][1];
            for (int v = 0; v < n; v++) {
                if (!used[v]) {
                    long dist = Math.abs(points[v][0] - ux) + Math.abs(points[v][1] - uy);
                    if (dist < best[v]) {
                        best[v] = dist;
                    }
                }
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(minCostConnectPoints(new long[][]{new long[]{0L, 0L}, new long[]{2L, 2L}, new long[]{3L, 10L}, new long[]{5L, 2L}, new long[]{7L, 0L}}));
    }
}
