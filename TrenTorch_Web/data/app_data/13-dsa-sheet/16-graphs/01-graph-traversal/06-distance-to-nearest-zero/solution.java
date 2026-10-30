import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Queue;

public class Main {
    // O(rows * cols) time, O(rows * cols) space
    static long[][] nearestZero(long[][] mat) {
        int rows = mat.length;
        int cols = rows > 0 ? mat[0].length : 0;
        long[][] dist = new long[rows][cols];
        Queue<int[]> queue = new ArrayDeque<>();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                dist[i][j] = -1;
            }
        }
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (mat[r][c] == 0) {
                    dist[r][c] = 0;
                    queue.offer(new int[]{r, c});
                }
            }
        }
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            int x = cell[0], y = cell[1];
            for (int[] d : dirs) {
                int nx = x + d[0];
                int ny = y + d[1];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && dist[nx][ny] == -1) {
                    dist[nx][ny] = dist[x][y] + 1;
                    queue.offer(new int[]{nx, ny});
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(nearestZero(new long[][]{new long[]{0L, 0L, 0L}, new long[]{0L, 1L, 0L}, new long[]{1L, 1L, 1L}})));
    }
}
