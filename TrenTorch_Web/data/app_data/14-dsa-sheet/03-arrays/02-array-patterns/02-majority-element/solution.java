public class Main {
    // O(n) time, O(1) space
    static long majorityElement(long[] nums) {
        long candidate = 0;
        int count = 0;
        for (long x : nums) {
            if (count == 0) {
                candidate = x;
            }
            if (x == candidate) {
                count++;
            } else {
                count--;
            }
        }
        int occurrences = 0;
        for (long x : nums) {
            if (x == candidate) {
                occurrences++;
            }
        }
        if (occurrences > nums.length / 2) {
            return candidate;
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(majorityElement(new long[]{2L, 2L, 1L, 1L, 2L, 2L, 3L}));
    }
}
