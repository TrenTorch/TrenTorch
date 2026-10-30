import java.util.Deque;
import java.util.ArrayDeque;

public class Main {
    // O(m*n) time, O(m*n) space where m=rows, n=cols
    static long orangesRotting(long[][] grid) {
        int rows = grid.length;
        if (rows == 0) return 0;
        int cols = grid[0].length;
        Deque<int[]> queue = new ArrayDeque<>();
        int fresh = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) {
                    queue.add(new int[]{r, c});
                } else if (grid[r][c] == 1) {
                    fresh++;
                }
            }
        }
        int minutes = 0;
        int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
        while (!queue.isEmpty() && fresh > 0) {
            minutes++;
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                int[] cell = queue.poll();
                for (int[] dir : dirs) {
                    int nx = cell[0] + dir[0];
                    int ny = cell[1] + dir[1];
                    if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 1) {
                        grid[nx][ny] = 2;
                        fresh--;
                        queue.add(new int[]{nx, ny});
                    }
                }
            }
        }
        return fresh == 0 ? minutes : -1;
    }

    public static void main(String[] args) {
        System.out.println(orangesRotting(new long[][]{new long[]{2L, 1L, 1L}, new long[]{1L, 1L, 0L}, new long[]{0L, 1L, 1L}}));
    }
}
