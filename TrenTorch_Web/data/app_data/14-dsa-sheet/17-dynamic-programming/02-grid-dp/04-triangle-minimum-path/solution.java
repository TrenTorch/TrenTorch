import java.util.Arrays;

public class Main {
    // O(n^2) time, O(n) space where n is the number of rows
    static long minimumTotal(long[][] triangle) {
        if (triangle == null || triangle.length == 0) {
            return 0;
        }
        long[] best = Arrays.copyOf(triangle[triangle.length - 1], triangle[triangle.length - 1].length);
        for (int row = triangle.length - 2; row >= 0; row--) {
            for (int j = 0; j <= row; j++) {
                best[j] = triangle[row][j] + Math.min(best[j], best[j + 1]);
            }
        }
        return best[0];
    }

    public static void main(String[] args) {
        System.out.println(minimumTotal(new long[][]{new long[]{2L}, new long[]{3L, 4L}, new long[]{6L, 5L, 7L}, new long[]{4L, 1L, 8L, 3L}}));
    }
}
