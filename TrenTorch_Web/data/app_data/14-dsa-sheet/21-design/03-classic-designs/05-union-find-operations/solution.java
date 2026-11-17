import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(q * alpha(n)) time for q operations, O(n) space
    static long[] runUnionFind(long n, String[] ops) {
        int size0 = (int) n;
        int[] parent = new int[size0];
        int[] size = new int[size0];
        for (int i = 0; i < size0; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("union")) {
                int a = find(parent, Integer.parseInt(parts[1]));
                int b = find(parent, Integer.parseInt(parts[2]));
                if (a != b) {
                    if (size[a] < size[b]) {
                        int tmp = a;
                        a = b;
                        b = tmp;
                    }
                    parent[b] = a;
                    size[a] += size[b];
                }
            } else if (parts[0].equals("connected")) {
                int x = find(parent, Integer.parseInt(parts[1]));
                int y = find(parent, Integer.parseInt(parts[2]));
                out.add(x == y ? 1L : 0L);
            } else {
                out.add((long) size[find(parent, Integer.parseInt(parts[1]))]);
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runUnionFind(5L, new String[]{"union 0 1", "union 1 2", "connected 0 2", "connected 0 3", "size 2"})));
    }
}
