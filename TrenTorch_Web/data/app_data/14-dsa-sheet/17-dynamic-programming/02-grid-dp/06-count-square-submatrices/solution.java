public class Main {
    // O(rows * cols) time, O(cols) space
    static long countSquares(long[][] matrix) {
        if (matrix == null || matrix.length == 0) {
            return 0;
        }
        int rows = matrix.length;
        int cols = matrix[0].length;
        long[] prev = new long[cols + 1];
        long total = 0;
        for (int r = 0; r < rows; r++) {
            long[] cur = new long[cols + 1];
            for (int c = 0; c < cols; c++) {
                if (matrix[r][c] == 1) {
                    cur[c + 1] = 1 + Math.min(prev[c], Math.min(prev[c + 1], cur[c]));
                    total += cur[c + 1];
                }
            }
            prev = cur;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countSquares(new long[][]{new long[]{0L, 1L, 1L, 1L}, new long[]{1L, 1L, 1L, 1L}, new long[]{0L, 1L, 1L, 1L}}));
    }
}
