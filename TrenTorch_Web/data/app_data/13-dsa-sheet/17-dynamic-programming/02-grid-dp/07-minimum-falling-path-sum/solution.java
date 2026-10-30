public class Main {
    // O(rows * cols) time, O(cols) space
    static long minFallingPathSum(long[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        int cols = matrix[0].length;
        long[] prev = matrix[0].clone();
        for (int r = 1; r < matrix.length; r++) {
            long[] cur = new long[cols];
            for (int c = 0; c < cols; c++) {
                long best = Long.MAX_VALUE;
                for (int k = Math.max(0, c - 1); k <= Math.min(cols - 1, c + 1); k++) {
                    best = Math.min(best, prev[k]);
                }
                cur[c] = matrix[r][c] + best;
            }
            prev = cur;
        }
        long result = Long.MAX_VALUE;
        for (long v : prev) {
            result = Math.min(result, v);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(minFallingPathSum(new long[][]{new long[]{2L, 1L, 3L}, new long[]{6L, 5L, 4L}, new long[]{7L, 8L, 9L}}));
    }
}
