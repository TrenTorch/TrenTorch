import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(2^(n/2) * n) time, O(2^(n/2)) space (meet in the middle)
    static long countSubsetSums(long[] nums, long k, long target) {
        int half = nums.length / 2;
        Map<Key, Long> left = sumsBySize(Arrays.copyOfRange(nums, 0, half));
        Map<Key, Long> right = sumsBySize(Arrays.copyOfRange(nums, half, nums.length));
        long count = 0;
        for (Map.Entry<Key, Long> entry : right.entrySet()) {
            Key r = entry.getKey();
            Long leftWays = left.get(new Key(k - r.size(), target - r.sum()));
            if (leftWays != null) {
                count += entry.getValue() * leftWays;
            }
        }
        return count;
    }

    // Maps (size, sum) to the number of subsets of values with that size and sum
    private static Map<Key, Long> sumsBySize(long[] values) {
        Map<Key, Long> states = new HashMap<>();
        states.put(new Key(0, 0), 1L);
        for (long v : values) {
            // copy first so that updates to states are not seen while iterating
            Map<Key, Long> snapshot = new HashMap<>(states);
            for (Map.Entry<Key, Long> e : snapshot.entrySet()) {
                Key key = e.getKey();
                states.merge(new Key(key.size() + 1, key.sum() + v), e.getValue(), Long::sum);
            }
        }
        return states;
    }

    private record Key(long size, long sum) {}

    public static void main(String[] args) {
        System.out.println(countSubsetSums(new long[]{1L, 2L, 3L, 4L}, 2L, 5L));
    }
}
