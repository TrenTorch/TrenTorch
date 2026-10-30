import java.util.*;

public class Main {
    // O((V+E) log V) time, O(V+E) space
    static long countShortestPaths(long n, long[][] roads) {
        final long MOD = 1_000_000_007L;
        int N = (int) n;
        List<List<int[]>> adj = new ArrayList<>(N);
        for (int i = 0; i < N; i++) adj.add(new ArrayList<>());
        for (long[] road : roads) {
            int a = (int) road[0];
            int b = (int) road[1];
            int t = (int) road[2];
            adj.get(a).add(new int[]{b, t});
            adj.get(b).add(new int[]{a, t});
        }
        long[] dist = new long[N];
        Arrays.fill(dist, Long.MAX_VALUE);
        long[] ways = new long[N];
        dist[0] = 0;
        ways[0] = 1;
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[]{0, 0});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d > dist[u]) continue;
            for (int[] edge : adj.get(u)) {
                int v = edge[0];
                int t = edge[1];
                long nd = d + t;
                if (nd < dist[v]) {
                    dist[v] = nd;
                    ways[v] = ways[u];
                    pq.offer(new long[]{nd, v});
                } else if (nd == dist[v]) {
                    ways[v] = (ways[v] + ways[u]) % MOD;
                }
            }
        }
        return ways[N - 1] % MOD;
    }

    public static void main(String[] args) {
        System.out.println(countShortestPaths(4L, new long[][]{new long[]{0L, 1L, 1L}, new long[]{0L, 2L, 1L}, new long[]{1L, 3L, 1L}, new long[]{2L, 3L, 1L}}));
    }
}
