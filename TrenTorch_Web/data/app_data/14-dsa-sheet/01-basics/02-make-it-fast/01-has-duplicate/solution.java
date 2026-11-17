import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(n) time, O(n) space
    static boolean hasDuplicate(long[] nums) {
        Set<Long> seen = new HashSet<>();
        for (long x : nums) {
            if (seen.contains(x)) {
                return true;
            }
            seen.add(x);
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(hasDuplicate(new long[]{1L, 2L, 3L, 1L}));
    }
}
