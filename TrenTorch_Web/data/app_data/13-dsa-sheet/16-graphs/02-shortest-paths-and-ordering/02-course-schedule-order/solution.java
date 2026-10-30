import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Main {
    // O((n + m) log n) time, O(n + m) space (n courses, m prerequisites)
    static long[] findOrder(long numCourses, long[][] prerequisites) {
        int n = (int) numCourses;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        int[] inDegree = new int[n];
        for (long[] pair : prerequisites) {
            int course = (int) pair[0];
            int pre = (int) pair[1];
            adj.get(pre).add(course);
            inDegree[course]++;
        }
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int v = 0; v < n; v++) {
            if (inDegree[v] == 0) {
                heap.add(v);
            }
        }
        long[] order = new long[n];
        int size = 0;
        while (!heap.isEmpty()) {
            int node = heap.poll();
            order[size++] = node;
            for (int nxt : adj.get(node)) {
                inDegree[nxt]--;
                if (inDegree[nxt] == 0) {
                    heap.add(nxt);
                }
            }
        }
        if (size != n) {
            return new long[0];
        }
        return order;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(findOrder(4L, new long[][]{new long[]{1L, 0L}, new long[]{2L, 0L}, new long[]{3L, 1L}, new long[]{3L, 2L}})));
    }
}
