public class Main {
    // O(rows * cols) time, O(cols) space
    static long minPathSum(long[][] grid) {
        int rows = grid.length;
        int cols = rows > 0 ? grid[0].length : 0;
        if (rows == 0 || cols == 0) {
            return 0;
        }
        long[] row = new long[cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (r == 0 && c == 0) {
                    row[c] = grid[0][0];
                } else if (r == 0) {
                    row[c] = row[c - 1] + grid[r][c];
                } else if (c == 0) {
                    row[c] = row[c] + grid[r][c];
                } else {
                    row[c] = Math.min(row[c], row[c - 1]) + grid[r][c];
                }
            }
        }
        return row[cols - 1];
    }

    public static void main(String[] args) {
        System.out.println(minPathSum(new long[][]{new long[]{1L, 3L, 1L}, new long[]{1L, 5L, 1L}, new long[]{4L, 2L, 1L}}));
    }
}
