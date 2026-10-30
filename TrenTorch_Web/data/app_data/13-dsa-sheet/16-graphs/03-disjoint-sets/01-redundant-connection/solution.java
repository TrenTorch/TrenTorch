public class Main {
    // O(n * alpha(n)) time, O(n) space (alpha = inverse Ackermann, n = number of edges)
    static long[] findRedundantConnection(long[][] edges) {
        int m = edges.length + 2;
        int[] parent = new int[m];
        int[] size = new int[m];
        for (int i = 0; i < m; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            int ra = find(parent, a);
            int rb = find(parent, b);
            if (ra == rb) {
                return new long[]{a, b};
            }
            if (size[ra] < size[rb]) {
                int tmp = ra;
                ra = rb;
                rb = tmp;
            }
            parent[rb] = ra;
            size[ra] += size[rb];
        }
        return new long[0];
    }

    static int find(int[] parent, int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(findRedundantConnection(new long[][]{new long[]{1L, 2L}, new long[]{1L, 3L}, new long[]{2L, 3L}})));
    }
}
