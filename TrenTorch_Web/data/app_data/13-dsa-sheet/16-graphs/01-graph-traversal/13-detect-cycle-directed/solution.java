import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(V + E) time, O(V + E) space
    static boolean hasCycleDirected(long n, long[][] edges) {
        List<List<Long>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        for (long[] edge : edges) {
            adj.get((int) edge[0]).add(edge[1]);
        }

        int[] state = new int[(int) n]; // 0 = unvisited, 1 = visiting, 2 = visited

        for (int start = 0; start < n; start++) {
            if (state[start] != 0) continue;

            state[start] = 1;
            List<int[]> stack = new ArrayList<>();
            stack.add(new int[]{start, 0});

            while (!stack.isEmpty()) {
                int[] frame = stack.get(stack.size() - 1);
                int node = frame[0];
                int i = frame[1];

                if (i < adj.get(node).size()) {
                    frame[1] = i + 1;
                    int nxt = adj.get(node).get(i).intValue();

                    if (state[nxt] == 1) {
                        return true;
                    }
                    if (state[nxt] == 0) {
                        state[nxt] = 1;
                        stack.add(new int[]{nxt, 0});
                    }
                } else {
                    state[node] = 2;
                    stack.remove(stack.size() - 1);
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(hasCycleDirected(3L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{2L, 0L}}));
    }
}
