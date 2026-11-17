import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(n) time, O(min(n, k)) space
    static boolean containsNearbyDuplicate(long[] nums, long k) {
        Set<Long> window = new HashSet<>();
        for (int i = 0; i < nums.length; i++) {
            if (window.contains(nums[i])) {
                return true;
            }
            window.add(nums[i]);
            if (i >= k) {
                window.remove(nums[(int) (i - k)]);
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(containsNearbyDuplicate(new long[]{1L, 2L, 3L, 1L}, 3L));
    }
}
