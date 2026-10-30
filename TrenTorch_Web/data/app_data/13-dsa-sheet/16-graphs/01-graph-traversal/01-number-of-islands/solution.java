import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(rows * cols) time, O(rows * cols) space
    static long numIslands(long[][] grid) {
        int rows = grid.length;
        if (rows == 0) return 0;
        int cols = grid[0].length;
        boolean[][] seen = new boolean[rows][cols];
        long count = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 1 && !seen[r][c]) {
                    count++;
                    seen[r][c] = true;
                    Deque<int[]> stack = new ArrayDeque<>();
                    stack.push(new int[]{r, c});
                    while (!stack.isEmpty()) {
                        int[] cell = stack.pop();
                        int x = cell[0];
                        int y = cell[1];
                        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
                        for (int[] d : dirs) {
                            int nx = x + d[0];
                            int ny = y + d[1];
                            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 1 && !seen[nx][ny]) {
                                seen[nx][ny] = true;
                                stack.push(new int[]{nx, ny});
                            }
                        }
                    }
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(numIslands(new long[][]{new long[]{1L, 1L, 0L}, new long[]{0L, 1L, 0L}, new long[]{0L, 0L, 1L}}));
    }
}
