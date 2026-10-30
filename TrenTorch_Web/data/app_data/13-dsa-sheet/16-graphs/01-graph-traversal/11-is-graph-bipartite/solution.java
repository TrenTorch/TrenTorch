import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n + m) time, O(n + m) space (n nodes, m edges)
    static boolean isBipartite(long n, long[][] edges) {
        int nodes = (int) n;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < nodes; i++) {
            adj.add(new ArrayList<>());
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            adj.get(a).add(b);
            adj.get(b).add(a);
        }
        int[] color = new int[nodes];
        Arrays.fill(color, -1);
        for (int start = 0; start < nodes; start++) {
            if (color[start] != -1) {
                continue;
            }
            color[start] = 0;
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            queue.add(start);
            while (!queue.isEmpty()) {
                int node = queue.poll();
                for (int nxt : adj.get(node)) {
                    if (color[nxt] == -1) {
                        color[nxt] = 1 - color[node];
                        queue.add(nxt);
                    } else if (color[nxt] == color[node]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isBipartite(4L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 3L}, new long[]{3L, 0L}}));
    }
}
