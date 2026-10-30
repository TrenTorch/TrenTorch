public class Main {
    // O(rows * cols) time, O(cols) space
    static long maximalRectangle(long[][] matrix) {
        if (matrix.length == 0) {
            return 0;
        }
        int cols = matrix[0].length;
        long[] heights = new long[cols];
        long best = 0;
        for (long[] row : matrix) {
            for (int j = 0; j < cols; j++) {
                heights[j] = row[j] != 0 ? heights[j] + 1 : 0;
            }
            best = Math.max(best, largestRectangle(heights));
        }
        return best;
    }

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
        System.out.println(maximalRectangle(new long[][]{new long[]{1L, 0L, 1L, 0L, 0L}, new long[]{1L, 0L, 1L, 1L, 1L}, new long[]{1L, 1L, 1L, 1L, 1L}, new long[]{1L, 0L, 0L, 1L, 0L}}));
    }
}
