import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

public class Main {
    // O(n log n) time, O(n) space
    static long minMeetingRooms(long[][] meetings) {
        if (meetings == null || meetings.length == 0) {
            return 0;
        }
        Arrays.sort(meetings, Comparator.comparingLong(a -> a[0]));
        PriorityQueue<Long> minHeap = new PriorityQueue<>();
        for (long[] meeting : meetings) {
            long start = meeting[0];
            long end = meeting[1];
            if (!minHeap.isEmpty() && minHeap.peek() <= start) {
                minHeap.poll();
            }
            minHeap.add(end);
        }
        return minHeap.size();
    }

    public static void main(String[] args) {
        System.out.println(minMeetingRooms(new long[][]{new long[]{0L, 30L}, new long[]{5L, 10L}, new long[]{15L, 20L}}));
    }
}
