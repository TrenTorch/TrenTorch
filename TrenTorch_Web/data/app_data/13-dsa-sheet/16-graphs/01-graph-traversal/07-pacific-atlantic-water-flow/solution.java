import java.util.ArrayList;
import java.util.List;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(m*n) time, O(m*n) space where m=rows, n=cols
    static long[][] pacificAtlantic(long[][] heights) {
        int rows = heights.length;
        if (rows == 0) return new long[0][];
        int cols = heights[0].length;
        if (cols == 0) return new long[0][];

        List<int[]> pacificStarts = new ArrayList<>();
        for (int r = 0; r < rows; r++) pacificStarts.add(new int[]{r, 0});
        for (int c = 0; c < cols; c++) pacificStarts.add(new int[]{0, c});

        List<int[]> atlanticStarts = new ArrayList<>();
        for (int r = 0; r < rows; r++) atlanticStarts.add(new int[]{r, cols - 1});
        for (int c = 0; c < cols; c++) atlanticStarts.add(new int[]{rows - 1, c});

        boolean[][] pacific = flood(heights, rows, cols, pacificStarts);
        boolean[][] atlantic = flood(heights, rows, cols, atlanticStarts);

        List<long[]> result = new ArrayList<>();
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (pacific[r][c] && atlantic[r][c]) {
                    result.add(new long[]{r, c});
                }
            }
        }
        return result.toArray(new long[0][]);
    }

    private static boolean[][] flood(long[][] heights, int rows, int cols, List<int[]> starts) {
        boolean[][] visited = new boolean[rows][cols];
        Deque<int[]> stack = new ArrayDeque<>();
        for (int[] start : starts) {
            int r = start[0], c = start[1];
            if (!visited[r][c]) {
                visited[r][c] = true;
                stack.push(start);
            }
        }
        int[] dr = {1, -1, 0, 0};
        int[] dc = {0, 0, 1, -1};
        while (!stack.isEmpty()) {
            int[] cur = stack.pop();
            int r = cur[0], c = cur[1];
            for (int i = 0; i < 4; i++) {
                int nr = r + dr[i];
                int nc = c + dc[i];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc] && heights[nr][nc] >= heights[r][c]) {
                    visited[nr][nc] = true;
                    stack.push(new int[]{nr, nc});
                }
            }
        }
        return visited;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(pacificAtlantic(new long[][]{new long[]{1L, 2L}, new long[]{2L, 1L}})));
    }
}
