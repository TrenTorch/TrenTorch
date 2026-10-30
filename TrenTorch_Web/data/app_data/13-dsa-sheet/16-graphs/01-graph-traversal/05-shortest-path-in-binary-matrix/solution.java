import java.util.ArrayDeque;

public class Main {
    // O(R*C) time, O(R*C) space (R rows, C columns)
    static long shortestPathBinaryMatrix(long[][] grid) {
        int rows = grid.length;
        int cols = rows > 0 ? grid[0].length : 0;
        if (rows == 0 || cols == 0 || grid[0][0] == 1 || grid[rows - 1][cols - 1] == 1) {
            return -1;
        }
        boolean[][] seen = new boolean[rows][cols];
        seen[0][0] = true;
        ArrayDeque<long[]> queue = new ArrayDeque<>();
        queue.add(new long[]{0, 0, 1});
        while (!queue.isEmpty()) {
            long[] cur = queue.poll();
            int x = (int) cur[0];
            int y = (int) cur[1];
            long steps = cur[2];
            if (x == rows - 1 && y == cols - 1) {
                return steps;
            }
            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    int nx = x + dx;
                    int ny = y + dy;
                    if (nx >= 0 && nx < rows && ny >= 0 && ny < cols
                            && grid[nx][ny] == 0 && !seen[nx][ny]) {
                        seen[nx][ny] = true;
                        queue.add(new long[]{nx, ny, steps + 1});
                    }
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(shortestPathBinaryMatrix(new long[][]{new long[]{0L, 0L, 0L}, new long[]{1L, 1L, 0L}, new long[]{1L, 1L, 0L}}));
    }
}
