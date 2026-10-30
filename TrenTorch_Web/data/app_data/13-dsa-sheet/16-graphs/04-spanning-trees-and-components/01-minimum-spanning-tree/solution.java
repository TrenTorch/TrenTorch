import java.util.Arrays;

public class Main {
    // O(m log m) time, O(n + m) space (n nodes, m edges)
    static long mstWeight(long n, long[][] edges) {
        int nodes = (int) n;
        int[] parent = new int[nodes];
        int[] size = new int[nodes];
        for (int i = 0; i < nodes; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        long[][] sorted = edges.clone();
        Arrays.sort(sorted, (long[] x, long[] y) -> Long.compare(x[2], y[2]));
        long total = 0;
        int taken = 0;
        for (long[] edge : sorted) {
            int ra = find(parent, (int) edge[0]);
            int rb = find(parent, (int) edge[1]);
            if (ra != rb) {
                if (size[ra] < size[rb]) {
                    int tmp = ra;
                    ra = rb;
                    rb = tmp;
                }
                parent[rb] = ra;
                size[ra] += size[rb];
                total += edge[2];
                taken++;
            }
        }
        return taken == nodes - 1 ? total : -1;
    }

    static int find(int[] parent, int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(mstWeight(4L, new long[][]{new long[]{0L, 1L, 1L}, new long[]{1L, 2L, 2L}, new long[]{2L, 3L, 3L}, new long[]{0L, 3L, 10L}, new long[]{0L, 2L, 5L}}));
    }
}
