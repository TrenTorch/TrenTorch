import java.util.PriorityQueue;

public class Main {
    // O(n log n) time, O(n) space
    static long furthestBuilding(long[] heights, long bricks, long ladders) {
        PriorityQueue<Long> minHeap = new PriorityQueue<>();
        for (int i = 1; i < heights.length; i++) {
            long climb = heights[i] - heights[i - 1];
            if (climb <= 0) continue;
            minHeap.add(climb);
            if (minHeap.size() > ladders) {
                bricks -= minHeap.poll();
                if (bricks < 0) {
                    return i - 1;
                }
            }
        }
        return heights.length - 1;
    }

    public static void main(String[] args) {
        System.out.println(furthestBuilding(new long[]{4L, 2L, 7L, 6L, 9L, 14L, 12L}, 5L, 1L));
    }
}
