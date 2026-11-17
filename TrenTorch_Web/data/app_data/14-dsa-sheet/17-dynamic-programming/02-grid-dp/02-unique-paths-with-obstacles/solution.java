public class Main {
    // O(rows * cols) time, O(cols) space
    static long uniquePathsObstacles(long[][] grid) {
        int rows = grid.length;
        if (rows == 0) return 0;
        int cols = grid[0].length;
        if (cols == 0) return 0;
        final long MOD = 1_000_000_007L;
        long[] row = new long[cols];
        row[0] = (grid[0][0] == 0) ? 1 : 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 1) {
                    row[c] = 0;
                } else if (c > 0) {
                    row[c] = (row[c] + row[c - 1]) % MOD;
                }
            }
        }
        return row[cols - 1];
    }

    public static void main(String[] args) {
        System.out.println(uniquePathsObstacles(new long[][]{new long[]{0L, 0L, 0L}, new long[]{0L, 1L, 0L}, new long[]{0L, 0L, 0L}}));
    }
}
