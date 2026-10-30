import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class Main {
    // O((n + m) log m) time, O(n + m) space (n nodes, m edges)
    static long[] shortestDistances(long n, long[][] edges, long source) {
        int nodes = (int) n;
        int src = (int) source;
        List<List<long[]>> adj = new ArrayList<>();
        for (int i = 0; i < nodes; i++) {
            adj.add(new ArrayList<>());
        }
        for (long[] edge : edges) {
            adj.get((int) edge[0]).add(new long[]{edge[1], edge[2]});
        }
        final long INF = Long.MAX_VALUE;
        long[] dist = new long[nodes];
        Arrays.fill(dist, INF);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
        heap.add(new long[]{0, src});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            long d = top[0];
            int u = (int) top[1];
            if (d > dist[u]) {
                continue;
            }
            for (long[] edge : adj.get(u)) {
                int v = (int) edge[0];
                long w = edge[1];
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    heap.add(new long[]{dist[v], v});
                }
            }
        }
        for (int i = 0; i < nodes; i++) {
            if (dist[i] == INF) {
                dist[i] = -1;
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(shortestDistances(3L, new long[][]{new long[]{0L, 1L, 4L}, new long[]{0L, 2L, 1L}, new long[]{2L, 1L, 2L}}, 0L)));
    }
}
