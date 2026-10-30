import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n log n) time, O(n) space
    static long insertionSortShifts(long[] nums) {
        if (nums == null || nums.length == 0) {
            return 0L;
        }
        int n = nums.length;
        // Coordinate compression
        long[] unique = Arrays.stream(nums).distinct().sorted().toArray();
        Map<Long, Integer> rank = new HashMap<>();
        for (int i = 0; i < unique.length; i++) {
            rank.put(unique[i], i + 1); // 1-indexed
        }
        int size = unique.length;
        int[] tree = new int[size + 1];
        long shifts = 0;
        for (int seen = 0; seen < n; seen++) {
            long x = nums[seen];
            int i = rank.get(x);
            // query BIT for prefix sum up to i
            int notBigger = 0;
            int idx = i;
            while (idx > 0) {
                notBigger += tree[idx];
                idx -= idx & -idx;
            }
            shifts += seen - notBigger;
            // update BIT at i
            idx = i;
            while (idx <= size) {
                tree[idx]++;
                idx += idx & -idx;
            }
        }
        return shifts;
    }

    public static void main(String[] args) {
        System.out.println(insertionSortShifts(new long[]{3L, 1L, 2L}));
    }
}
