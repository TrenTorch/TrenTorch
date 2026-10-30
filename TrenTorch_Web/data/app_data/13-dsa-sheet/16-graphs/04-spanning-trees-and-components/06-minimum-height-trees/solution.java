import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    static long[] minHeightTrees(long n, long[][] edges) {
        int size = (int) n;
        if (size <= 2) {
            long[] result = new long[size];
            for (int i = 0; i < size; i++) {
                result[i] = i;
            }
            return result;
        }
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            adj.add(new ArrayList<>());
        }
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            adj.get(a).add(b);
            adj.get(b).add(a);
        }
        int[] degree = new int[size];
        List<Integer> leaves = new ArrayList<>();
        for (int v = 0; v < size; v++) {
            degree[v] = adj.get(v).size();
            if (degree[v] == 1) {
                leaves.add(v);
            }
        }
        long remaining = n;
        while (remaining > 2) {
            remaining -= leaves.size();
            List<Integer> next = new ArrayList<>();
            for (int leaf : leaves) {
                for (int other : adj.get(leaf)) {
                    degree[other]--;
                    if (degree[other] == 1) {
                        next.add(other);
                    }
                }
            }
            leaves = next;
        }
        Collections.sort(leaves);
        long[] result = new long[leaves.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = leaves.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(minHeightTrees(6L, new long[][]{new long[]{3L, 0L}, new long[]{3L, 1L}, new long[]{3L, 2L}, new long[]{3L, 4L}, new long[]{5L, 4L}})));
    }
}
