import java.util.*;

public class Main {
    // O(4^(R*C)) time in the worst case (every simple path is explored), O(R * C) space for the path and marks
    static String[] ratInAMaze(long[][] maze) {
        int rows = maze.length;
        int cols = rows > 0 ? maze[0].length : 0;
        if (rows == 0 || cols == 0 || maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0) {
            return new String[0];
        }
        List<String> out = new ArrayList<>();
        ratGo(maze, rows, cols, 0, 0, new StringBuilder(), new boolean[rows][cols], out);
        return out.toArray(new String[0]);
    }

    static void ratGo(long[][] maze, int rows, int cols, int r, int c,
                      StringBuilder path, boolean[][] onPath, List<String> out) {
        if (r == rows - 1 && c == cols - 1) {
            out.add(path.toString());
            return;
        }
        onPath[r][c] = true;
        String letters = "DLRU";
        int[] dr = {1, 0, 0, -1};
        int[] dc = {0, -1, 1, 0};
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k];
            int nc = c + dc[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                    && maze[nr][nc] == 1L && !onPath[nr][nc]) {
                path.append(letters.charAt(k));
                ratGo(maze, rows, cols, nr, nc, path, onPath, out);
                path.setLength(path.length() - 1);
            }
        }
        onPath[r][c] = false;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(ratInAMaze(new long[][]{
                new long[]{1L, 0L, 0L, 0L},
                new long[]{1L, 1L, 0L, 1L},
                new long[]{1L, 1L, 0L, 0L},
                new long[]{0L, 1L, 1L, 1L}})));
    }
}
