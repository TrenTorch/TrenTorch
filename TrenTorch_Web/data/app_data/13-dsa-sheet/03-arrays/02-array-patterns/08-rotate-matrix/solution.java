import java.util.Arrays;

public class Main {
    // O(rows * cols) time, O(rows * cols) space
    static long[][] rotateMatrix(long[][] matrix) {
        int m = matrix.length;
        if (m == 0) {
            return new long[0][];
        }
        int n = matrix[0].length;
        long[][] out = new long[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                out[i][j] = matrix[m - 1 - j][i];
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.deepToString(rotateMatrix(new long[][]{new long[]{1L, 2L, 3L}, new long[]{4L, 5L, 6L}})));
    }
}
