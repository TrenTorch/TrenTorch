public class Main {
    // O(n) time, O(n) space
    static long largestRectangle(long[] heights) {
        int n = heights.length;
        long best = 0;
        int[] stack = new int[n + 1];
        int top = 0;
        for (int i = 0; i <= n; i++) {
            long h = i < n ? heights[i] : 0;
            while (top > 0 && heights[stack[top - 1]] >= h) {
                long height = heights[stack[--top]];
                int left = top > 0 ? stack[top - 1] : -1;
                best = Math.max(best, height * (i - left - 1));
            }
            stack[top++] = i;
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(largestRectangle(new long[]{2L, 1L, 5L, 6L, 2L, 3L}));
    }
}
