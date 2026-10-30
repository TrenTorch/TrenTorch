import java.util.PriorityQueue;

public class Main {
    // O(n log n) time, O(n) space
    static long minRefuelStops(long target, long startFuel, long[][] stations) {
        PriorityQueue<Long> maxHeap = new PriorityQueue<>();
        long reach = startFuel;
        int stops = 0;
        int i = 0;
        int n = stations.length;
        while (reach < target) {
            while (i < n && stations[i][0] <= reach) {
                maxHeap.offer(-stations[i][1]);
                i++;
            }
            if (maxHeap.isEmpty()) {
                return -1;
            }
            reach += -maxHeap.poll();
            stops++;
        }
        return stops;
    }

    public static void main(String[] args) {
        System.out.println(minRefuelStops(100L, 10L, new long[][]{new long[]{10L, 60L}, new long[]{20L, 30L}, new long[]{30L, 30L}, new long[]{60L, 40L}}));
    }
}
