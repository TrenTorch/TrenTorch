import java.util.ArrayDeque;

public class Main {
    // O(rows * cols) time, O(rows * cols) space
    static long maxIslandArea(long[][] grid) {
        int rows = grid.length;
        if (rows == 0) return 0;
        int cols = grid[0].length;
        boolean[][] seen = new boolean[rows][cols];
        long best = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 1 && !seen[r][c]) {
                    seen[r][c] = true;
                    ArrayDeque<int[]> stack = new ArrayDeque<>();
                    stack.push(new int[]{r, c});
                    long size = 0;
                    while (!stack.isEmpty()) {
                        int[] cell = stack.pop();
                        int x = cell[0];
                        int y = cell[1];
                        size++;
                        int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
                        for (int[] dir : directions) {
                            int nx = x + dir[0];
                            int ny = y + dir[1];
                            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 1 && !seen[nx][ny]) {
                                seen[nx][ny] = true;
                                stack.push(new int[]{nx, ny});
                            }
                        }
                    }
                    if (size > best) best = size;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxIslandArea(new long[][]{new long[]{1L, 1L, 0L}, new long[]{0L, 1L, 0L}, new long[]{0L, 0L, 1L}}));
    }
}
