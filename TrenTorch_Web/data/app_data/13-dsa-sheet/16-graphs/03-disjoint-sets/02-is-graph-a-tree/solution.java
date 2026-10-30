public class Main {
    // O(n α(n)) time, O(n) space
    static boolean validTree(long n, long[][] edges) {
        if (n == 0 || edges.length != n - 1) {
            return false;
        }
        int N = (int) n;
        int[] parent = new int[N];
        int[] size = new int[N];
        for (int i = 0; i < N; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            int ra = find(parent, a);
            int rb = find(parent, b);
            if (ra == rb) {
                return false;
            }
            if (size[ra] < size[rb]) {
                int temp = ra;
                ra = rb;
                rb = temp;
            }
            parent[rb] = ra;
            size[ra] += size[rb];
        }
        return true;
    }

    private static int find(int[] parent, int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(validTree(5L, new long[][]{new long[]{0L, 1L}, new long[]{0L, 2L}, new long[]{0L, 3L}, new long[]{1L, 4L}}));
    }
}
