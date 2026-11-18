import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

public class Main {
    // O(n log n) time, O(n) space
    static long findMaximizedCapital(long k, long w, long[] profits, long[] capital) {
        int n = profits.length;
        long[][] projects = new long[n][2];
        for (int i = 0; i < n; i++) {
            projects[i][0] = capital[i];
            projects[i][1] = profits[i];
        }
        Arrays.sort(projects, Comparator.comparingLong(a -> a[0]));

        PriorityQueue<Long> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        int i = 0;
        for (long iter = 0; iter < k; iter++) {
            while (i < n && projects[i][0] <= w) {
                maxHeap.offer(projects[i][1]);
                i++;
            }
            if (maxHeap.isEmpty()) {
                break;
            }
            w += maxHeap.poll();
        }
        return w;
    }

    public static void main(String[] args) {
        System.out.println(findMaximizedCapital(2L, 0L, new long[]{1L, 2L, 3L}, new long[]{0L, 1L, 1L}));
    }
}
