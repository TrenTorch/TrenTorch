import java.util.PriorityQueue;

public class Main {
    // O(N log N) time, O(N) space where N = rows * cols
    static long swimInWater(long[][] grid) {
        int n = grid.length;
        int m = grid[0].length;
        boolean[][] seen = new boolean[n][m];
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[]{grid[0][0], 0, 0});
        seen[0][0] = true;
        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long t = cur[0];
            int x = (int) cur[1];
            int y = (int) cur[2];
            if (x == n - 1 && y == m - 1) {
                return t;
            }
            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i];
                int ny = y + dy[i];
                if (nx >= 0 && nx < n && ny >= 0 && ny < m && !seen[nx][ny]) {
                    seen[nx][ny] = true;
                    long nt = Math.max(t, grid[nx][ny]);
                    pq.offer(new long[]{nt, nx, ny});
                }
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(swimInWater(new long[][]{new long[]{0L, 2L}, new long[]{1L, 3L}}));
    }
}
