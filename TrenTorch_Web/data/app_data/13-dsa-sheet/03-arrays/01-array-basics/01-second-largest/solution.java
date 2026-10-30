public class Main {
    // O(n) time, O(1) space
    static long secondLargest(long[] nums) {
        long largest = -1;
        long second = -1;
        for (long x : nums) {
            if (largest == -1 || x > largest) {
                second = largest;
                largest = x;
            } else if (x < largest && (second == -1 || x > second)) {
                second = x;
            }
        }
        return second == -1 ? -1 : second;
    }

    public static void main(String[] args) {
        System.out.println(secondLargest(new long[]{4L, 9L, 9L, 6L}));
    }
}
