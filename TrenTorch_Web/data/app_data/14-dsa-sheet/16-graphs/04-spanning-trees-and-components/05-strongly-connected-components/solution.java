import java.util.ArrayList;
import java.util.ArrayDeque;
import java.util.List;
import java.util.Deque;

public class Main {
    // O(V+E) time, O(V+E) space
    static long countScc(long n, long[][] edges) {
        int N = (int) n;
        List<Integer>[] adj = new List[N];
        List<Integer>[] rev = new List[N];
        for (int i = 0; i < N; i++) {
            adj[i] = new ArrayList<>();
            rev[i] = new ArrayList<>();
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            adj[a].add(b);
            rev[b].add(a);
        }

        boolean[] seen = new boolean[N];
        List<Integer> order = new ArrayList<>(N);

        // First pass: compute post-order
        for (int start = 0; start < N; start++) {
            if (seen[start]) continue;
            seen[start] = true;
            Deque<int[]> stack = new ArrayDeque<>();
            stack.push(new int[]{start, 0});
            while (!stack.isEmpty()) {
                int[] top = stack.peek();
                int node = top[0];
                int i = top[1];
                if (i < adj[node].size()) {
                    int nxt = adj[node].get(i);
                    top[1] = i + 1;
                    if (!seen[nxt]) {
                        seen[nxt] = true;
                        stack.push(new int[]{nxt, 0});
                    }
                } else {
                    stack.pop();
                    order.add(node);
                }
            }
        }

        // Second pass: count SCCs on reversed graph
        seen = new boolean[N];
        int count = 0;
        for (int idx = order.size() - 1; idx >= 0; idx--) {
            int start = order.get(idx);
            if (seen[start]) continue;
            count++;
            seen[start] = true;
            Deque<Integer> stack2 = new ArrayDeque<>();
            stack2.push(start);
            while (!stack2.isEmpty()) {
                int node = stack2.pop();
                for (int nxt : rev[node]) {
                    if (!seen[nxt]) {
                        seen[nxt] = true;
                        stack2.push(nxt);
                    }
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countScc(5L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}, new long[]{1L, 3L}, new long[]{3L, 4L}}));
    }
}
