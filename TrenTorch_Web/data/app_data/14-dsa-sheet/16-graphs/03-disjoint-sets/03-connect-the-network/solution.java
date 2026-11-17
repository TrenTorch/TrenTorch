public class Main {
    // O(n + m * alpha(n)) time, O(n) space (n computers, m connections)
    static long makeConnected(long n, long[][] connections) {
        if (connections.length < n - 1) {
            return -1;
        }
        int nodes = (int) n;
        int[] parent = new int[nodes];
        int[] size = new int[nodes];
        for (int i = 0; i < nodes; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        long components = n;
        for (long[] connection : connections) {
            int ra = find(parent, (int) connection[0]);
            int rb = find(parent, (int) connection[1]);
            if (ra != rb) {
                if (size[ra] < size[rb]) {
                    int tmp = ra;
                    ra = rb;
                    rb = tmp;
                }
                parent[rb] = ra;
                size[ra] += size[rb];
                components--;
            }
        }
        return components - 1;
    }

    static int find(int[] parent, int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(makeConnected(4L, new long[][]{new long[]{0L, 1L}, new long[]{0L, 2L}, new long[]{1L, 2L}}));
    }
}
