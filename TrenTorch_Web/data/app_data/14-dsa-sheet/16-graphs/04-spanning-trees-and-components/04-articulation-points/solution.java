import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n + m) time, O(n + m) space
    static long[] articulationPoints(long n, long[][] edges) {
        int N = (int) n;
        List<Integer>[] adj = new List[N];
        for (int i = 0; i < N; i++) {
            adj[i] = new ArrayList<>();
        }
        for (long[] e : edges) {
            int u = (int) e[0];
            int v = (int) e[1];
            adj[u].add(v);
            adj[v].add(u);
        }

        int[] disc = new int[N];
        int[] low = new int[N];
        boolean[] isCut = new boolean[N];
        Arrays.fill(disc, -1);
        int timer = 0;

        for (int root = 0; root < N; root++) {
            if (disc[root] != -1) continue;
            disc[root] = low[root] = timer++;
            int rootChildren = 0;
            ArrayDeque<int[]> stack = new ArrayDeque<>();
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
                        if (node == root) rootChildren++;
                        stack.push(new int[]{nxt, node, 0});
                    } else {
                        low[node] = Math.min(low[node], disc[nxt]);
                    }
                } else if (parent != -1) {
                    low[parent] = Math.min(low[parent], low[node]);
                    if (parent != root && low[node] >= disc[parent]) {
                        isCut[parent] = true;
                    }
                }
            }

            if (rootChildren >= 2) {
                isCut[root] = true;
            }
        }

        List<Long> result = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            if (isCut[i]) result.add((long) i);
        }
        long[] ans = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            ans[i] = result.get(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(articulationPoints(5L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}, new long[]{1L, 3L}, new long[]{3L, 4L}})));
    }
}
