import java.util.PriorityQueue;

public class Main {
    // O(N log k) time, O(N + k) space where N is total elements, k is number of lists
    static long[] mergeSortedLists(long[][] lists) {
        int total = 0;
        for (long[] list : lists) {
            total += list.length;
        }
        long[] result = new long[total];
        if (total == 0) {
            return result;
        }

        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));

        for (int i = 0; i < lists.length; i++) {
            if (lists[i].length > 0) {
                pq.add(new long[]{lists[i][0], i, 0});
            }
        }

        int idx = 0;
        while (!pq.isEmpty()) {
            long[] curr = pq.poll();
            result[idx++] = curr[0];
            int listIdx = (int) curr[1];
            int elemIdx = (int) curr[2];
            if (elemIdx + 1 < lists[listIdx].length) {
                pq.add(new long[]{lists[listIdx][elemIdx + 1], listIdx, elemIdx + 1});
            }
        }

        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(mergeSortedLists(new long[][]{new long[]{1L, 4L, 7L}, new long[]{2L, 5L}, new long[]{3L, 6L, 9L}})));
    }
}
