import java.util.ArrayList;
import java.util.List;
import java.util.Deque;
import java.util.ArrayDeque;

public class Main {
    // O(n + m) time, O(n + m) space
    static boolean hasCycleUndirected(long n, long[][] edges) {
        int N = (int) n;
        List<int[]>[] adj = new ArrayList[N];
        for (int i = 0; i < N; i++) {
            adj[i] = new ArrayList<>();
        }
        for (int i = 0; i < edges.length; i++) {
            long a = edges[i][0];
            long b = edges[i][1];
            if (a == b) {
                return true;
            }
            int u = (int) a;
            int v = (int) b;
            adj[u].add(new int[]{v, i});
            adj[v].add(new int[]{u, i});
        }
        boolean[] seen = new boolean[N];
        for (int start = 0; start < N; start++) {
            if (seen[start]) continue;
            seen[start] = true;
            Deque<int[]> stack = new ArrayDeque<>();
            stack.push(new int[]{start, -1});
            while (!stack.isEmpty()) {
                int[] cur = stack.pop();
                int node = cur[0];
                int via = cur[1];
                for (int[] edge : adj[node]) {
                    int nxt = edge[0];
                    int edgeId = edge[1];
                    if (edgeId == via) continue;
                    if (seen[nxt]) {
                        return true;
                    }
                    seen[nxt] = true;
                    stack.push(new int[]{nxt, edgeId});
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(hasCycleUndirected(4L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}, new long[]{3L, 3L}}));
    }
}
