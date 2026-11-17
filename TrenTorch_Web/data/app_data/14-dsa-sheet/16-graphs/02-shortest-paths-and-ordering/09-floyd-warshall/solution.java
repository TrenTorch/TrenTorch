import java.util.Arrays;

public class Main {
    // O(n^3) time, O(n^2) space (n nodes)
    static long[][] allPairsShortest(long n, long[][] edges) {
        int nodes = (int) n;
        final long INF = Long.MAX_VALUE / 4;
        long[][] dist = new long[nodes][nodes];
        for (int i = 0; i < nodes; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0;
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            long w = edge[2];
            if (w < dist[a][b]) {
                dist[a][b] = w;
            }
        }
        for (int k = 0; k < nodes; k++) {
            long[] rowK = dist[k];
            for (int i = 0; i < nodes; i++) {
                long dik = dist[i][k];
                if (dik == INF) {
                    continue;
                }
                long[] rowI = dist[i];
                for (int j = 0; j < nodes; j++) {
                    if (dik + rowK[j] < rowI[j]) {
                        rowI[j] = dik + rowK[j];
                    }
                }
            }
        }
        for (int i = 0; i < nodes; i++) {
            for (int j = 0; j < nodes; j++) {
                if (dist[i][j] >= INF) {
                    dist[i][j] = -1;
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(allPairsShortest(3L, new long[][]{new long[]{0L, 1L, 4L}, new long[]{1L, 2L, 1L}, new long[]{0L, 2L, 7L}})));
    }
}
