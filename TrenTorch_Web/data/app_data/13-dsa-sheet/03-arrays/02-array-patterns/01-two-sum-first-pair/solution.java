import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(n) space
    static long[] twoSumFirstPair(long[] nums, long target) {
        Map<Long, Integer> first = new HashMap<>();
        int bestI = -1, bestJ = -1;
        for (int j = 0; j < nums.length; j++) {
            long x = nums[j];
            Long complement = target - x;
            if (first.containsKey(complement)) {
                int i = first.get(complement);
                if (bestI == -1 || i < bestI || (i == bestI && j < bestJ)) {
                    bestI = i;
                    bestJ = j;
                }
            }
            if (!first.containsKey(x)) {
                first.put(x, j);
            }
        }
        if (bestI == -1) {
            return new long[]{-1, -1};
        } else {
            return new long[]{bestI, bestJ};
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(twoSumFirstPair(new long[]{1L, 6L, 5L, 3L, 8L}, 9L)));
    }
}
