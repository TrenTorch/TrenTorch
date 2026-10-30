public class Main {
    // O(n) time, O(1) space
    static long trapWater(long[] heights) {
        int left = 0;
        int right = heights.length - 1;
        long leftMax = 0;
        long rightMax = 0;
        long total = 0;
        while (left < right) {
            if (heights[left] < heights[right]) {
                if (heights[left] > leftMax) {
                    leftMax = heights[left];
                }
                total += leftMax - heights[left];
                left++;
            } else {
                if (heights[right] > rightMax) {
                    rightMax = heights[right];
                }
                total += rightMax - heights[right];
                right--;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(trapWater(new long[]{0L, 1L, 0L, 2L, 1L, 0L, 1L, 3L, 2L, 1L, 2L, 1L}));
    }
}
