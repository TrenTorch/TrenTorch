import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class Main {
    // O(V + E) time, O(V + E) space
    static boolean canFinish(long numCourses, long[][] prerequisites) {
        int n = (int) numCourses;
        List<Integer>[] adj = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            adj[i] = new ArrayList<>();
        }
        int[] inDegree = new int[n];
        for (long[] pair : prerequisites) {
            int course = (int) pair[0];
            int pre = (int) pair[1];
            adj[pre].add(course);
            inDegree[course]++;
        }
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < n; i++) {
            if (inDegree[i] == 0) {
                queue.add(i);
            }
        }
        int taken = 0;
        while (!queue.isEmpty()) {
            int node = queue.poll();
            taken++;
            for (int nxt : adj[node]) {
                inDegree[nxt]--;
                if (inDegree[nxt] == 0) {
                    queue.add(nxt);
                }
            }
        }
        return taken == n;
    }

    public static void main(String[] args) {
        System.out.println(canFinish(2L, new long[][]{new long[]{1L, 0L}}));
    }
}
