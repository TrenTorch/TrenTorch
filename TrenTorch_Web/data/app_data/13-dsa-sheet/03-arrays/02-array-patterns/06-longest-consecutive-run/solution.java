import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(n) expected time (hash set), O(n) space
    static long longestConsecutive(long[] nums) {
        Set<Long> values = new HashSet<>();
        for (long x : nums) {
            values.add(x);
        }
        long best = 0;
        for (long x : values) {
            if (!values.contains(x - 1)) {
                long length = 1;
                while (values.contains(x + length)) {
                    length++;
                }
                best = Math.max(best, length);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestConsecutive(new long[]{100L, 4L, 200L, 1L, 3L, 2L}));
    }
}
