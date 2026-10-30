import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

public class Main {
    // O(n + m) time, O(n + m) space
    static long[] eventualSafeNodes(long n, long[][] edges) {
        int N = (int) n;
        List<Integer>[] rev = new List[N];
        for (int i = 0; i < N; i++) {
            rev[i] = new ArrayList<>();
        }
        int[] outDegree = new int[N];
        for (long[] edge : edges) {
            int a = (int) edge[0];
            int b = (int) edge[1];
            rev[b].add(a);
            outDegree[a]++;
        }
        Deque<Integer> queue = new LinkedList<>();
        for (int i = 0; i < N; i++) {
            if (outDegree[i] == 0) {
                queue.add(i);
            }
        }
        boolean[] safe = new boolean[N];
        while (!queue.isEmpty()) {
            int node = queue.poll();
            safe[node] = true;
            for (int p : rev[node]) {
                outDegree[p]--;
                if (outDegree[p] == 0) {
                    queue.add(p);
                }
            }
        }
        List<Long> result = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            if (safe[i]) {
                result.add((long) i);
            }
        }
        long[] resArray = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            resArray[i] = result.get(i);
        }
        return resArray;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(eventualSafeNodes(7L, new long[][]{new long[]{0L, 1L}, new long[]{0L, 2L}, new long[]{1L, 2L}, new long[]{1L, 3L}, new long[]{2L, 5L}, new long[]{3L, 0L}, new long[]{4L, 5L}})));
    }
}
