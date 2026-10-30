import java.util.ArrayList;
import java.util.List;
import java.util.Deque;
import java.util.ArrayDeque;

public class Main {
    // O(n + m) time, O(n + m) space
    static boolean validPath(long n, long[][] edges, long source, long destination) {
        int N = (int) n;
        List<Integer>[] adj = new ArrayList[N];
        for (int i = 0; i < N; i++) {
            adj[i] = new ArrayList<>();
        }
        for (long[] edge : edges) {
            int u = (int) edge[0];
            int v = (int) edge[1];
            adj[u].add(v);
            adj[v].add(u);
        }
        boolean[] seen = new boolean[N];
        int src = (int) source;
        int dest = (int) destination;
        seen[src] = true;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(src);
        while (!stack.isEmpty()) {
            int node = stack.pop();
            if (node == dest) {
                return true;
            }
            for (int nxt : adj[node]) {
                if (!seen[nxt]) {
                    seen[nxt] = true;
                    stack.push(nxt);
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(validPath(3L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}}, 0L, 2L));
    }
}
