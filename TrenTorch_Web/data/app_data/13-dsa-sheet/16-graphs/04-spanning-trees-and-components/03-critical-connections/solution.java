import java.util.*;

public class Main {
    // O(V + E) time, O(V + E) space
    static long[][] criticalConnections(long n, long[][] connections) {
        int N = (int) n;
        List<Integer>[] adj = new ArrayList[N];
        for (int i = 0; i < N; i++) {
            adj[i] = new ArrayList<>();
        }
        for (long[] edge : connections) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            adj[a].add(b);
            adj[b].add(a);
        }

        int[] disc = new int[N];
        int[] low = new int[N];
        Arrays.fill(disc, -1);
        List<long[]> bridges = new ArrayList<>();
        int timer = 0;

        for (int root = 0; root < N; root++) {
            if (disc[root] != -1) continue;
            disc[root] = low[root] = timer++;
            Deque<int[]> stack = new ArrayDeque<>();
            stack.push(new int[]{root, -1, 0});

            while (!stack.isEmpty()) {
                int[] top = stack.pop();
                int node = top[0];
                int parent = top[1];
                int i = top[2];

                if (i < adj[node].size()) {
                    stack.push(new int[]{node, parent, i + 1});
                    int nxt = adj[node].get(i);
                    if (nxt == parent) continue;
                    if (disc[nxt] == -1) {
                        disc[nxt] = low[nxt] = timer++;
                        stack.push(new int[]{nxt, node, 0});
                    } else {
                        low[node] = Math.min(low[node], disc[nxt]);
                    }
                } else if (parent != -1) {
                    low[parent] = Math.min(low[parent], low[node]);
                    if (low[node] > disc[parent]) {
                        long a = Math.min(parent, node);
                        long b = Math.max(parent, node);
                        bridges.add(new long[]{a, b});
                    }
                }
            }
        }

        bridges.sort((a, b) -> {
            if (a[0] != b[0]) return Long.compare(a[0], b[0]);
            return Long.compare(a[1], b[1]);
        });

        return bridges.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(criticalConnections(4L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}, new long[]{1L, 3L}})));
    }
}
