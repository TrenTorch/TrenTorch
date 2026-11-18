import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n + m) time, O(n + m) space (n nodes, m edges)
    static long countComponents(long n, long[][] edges) {
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
        boolean[] seen = new boolean[nodes];
        long count = 0;
        for (int start = 0; start < nodes; start++) {
            if (seen[start]) {
                continue;
            }
            count++;
            seen[start] = true;
            ArrayDeque<Integer> stack = new ArrayDeque<>();
            stack.push(start);
            while (!stack.isEmpty()) {
                int node = stack.pop();
                for (int nxt : adj.get(node)) {
                    if (!seen[nxt]) {
                        seen[nxt] = true;
                        stack.push(nxt);
                    }
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countComponents(5L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{3L, 4L}}));
    }
}
