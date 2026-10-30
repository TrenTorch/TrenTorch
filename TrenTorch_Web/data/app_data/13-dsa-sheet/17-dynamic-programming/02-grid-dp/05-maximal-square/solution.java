public class Main {
    // O(m*n) time, O(n) space where m = rows, n = cols
    static long maximalSquare(long[][] matrix) {
        int rows = matrix.length;
        if (rows == 0) return 0;
        int cols = matrix[0].length;
        long[] prev = new long[cols + 1];
        long best = 0;
        for (int r = 0; r < rows; r++) {
            long[] cur = new long[cols + 1];
            for (int c = 0; c < cols; c++) {
                if (matrix[r][c] == 1L) {
                    cur[c + 1] = 1 + Math.min(prev[c], Math.min(prev[c + 1], cur[c]));
                    if (cur[c + 1] > best) best = cur[c + 1];
                }
            }
            prev = cur;
        }
        return best * best;
    }

    public static void main(String[] args) {
        System.out.println(maximalSquare(new long[][]{new long[]{1L, 0L, 1L, 0L, 0L}, new long[]{1L, 0L, 1L, 1L, 1L}, new long[]{1L, 1L, 1L, 1L, 1L}, new long[]{1L, 0L, 0L, 1L, 0L}}));
    }
}
