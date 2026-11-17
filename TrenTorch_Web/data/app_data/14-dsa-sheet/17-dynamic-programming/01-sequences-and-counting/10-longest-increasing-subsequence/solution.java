public class Main {
    // O(n log n) time, O(n) space
    static long lengthOfLis(long[] nums) {
        long[] tails = new long[nums.length];
        int size = 0;
        for (long x : nums) {
            int lo = 0;
            int hi = size;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (tails[mid] < x) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            tails[lo] = x;
            if (lo == size) {
                size++;
            }
        }
        return size;
    }

    public static void main(String[] args) {
        System.out.println(lengthOfLis(new long[]{10L, 9L, 2L, 5L, 3L, 7L, 101L, 18L}));
    }
}
