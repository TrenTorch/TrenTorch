import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(colors^n) time, O(n + e) space
    static boolean canColorGraph(long n, long[][] edges, long colors) {
        // Check for self-loops
        for (long[] edge : edges) {
            if (edge[0] == edge[1]) {
                return false;
            }
        }

        int nInt = (int) n;
        int colorsInt = (int) colors;

        // Build adjacency list
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < nInt; i++) {
            adj.add(new ArrayList<>());
        }
        for (long[] edge : edges) {
            int u = (int) edge[0];
            int v = (int) edge[1];
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] color = new int[nInt];
        for (int i = 0; i < nInt; i++) {
            color[i] = -1;
        }

        return dfs(0, adj, color, colorsInt, nInt);
    }

    private static boolean dfs(int i, List<List<Integer>> adj, int[] color, int colors, int n) {
        if (i == n) {
            return true;
        }
        for (int c = 0; c < colors; c++) {
            boolean ok = true;
            for (int neighbor : adj.get(i)) {
                if (color[neighbor] == c) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                color[i] = c;
                if (dfs(i + 1, adj, color, colors, n)) {
                    return true;
                }
                color[i] = -1;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(canColorGraph(3L, new long[][]{new long[]{0L, 1L}, new long[]{1L, 2L}, new long[]{0L, 2L}}, 3L));
    }
}
