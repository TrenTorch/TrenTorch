import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Arrays;

public class Main {
    // O(rows * cols) time, O(rows * cols) space
    static long[][] floodFill(long[][] image, long sr, long sc, long color) {
        int startRow = (int) sr;
        int startCol = (int) sc;
        long old = image[startRow][startCol];
        if (old == color) {
            return image;
        }
        int rows = image.length;
        int cols = image[0].length;
        image[startRow][startCol] = color;
        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{startRow, startCol});
        while (!stack.isEmpty()) {
            int[] cur = stack.pop();
            int x = cur[0];
            int y = cur[1];
            // four directions
            int[][] dirs = {{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}};
            for (int[] next : dirs) {
                int nx = next[0];
                int ny = next[1];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && image[nx][ny] == old) {
                    image[nx][ny] = color;
                    stack.push(new int[]{nx, ny});
                }
            }
        }
        return image;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(floodFill(new long[][]{new long[]{1L, 1L, 1L}, new long[]{1L, 1L, 0L}, new long[]{1L, 0L, 1L}}, 1L, 1L, 2L)));
    }
}
