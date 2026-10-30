public class Main {
    // O(n) time, O(1) space
    static long maxWater(long[] heights) {
        int left = 0;
        int right = heights.length - 1;
        long best = 0;
        while (left < right) {
            long area = Math.min(heights[left], heights[right]) * (right - left);
            if (area > best) best = area;
            if (heights[left] < heights[right]) {
                left++;
            } else {
                right--;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxWater(new long[]{1L, 8L, 6L, 2L, 5L, 4L, 8L, 3L, 7L}));
    }
}
