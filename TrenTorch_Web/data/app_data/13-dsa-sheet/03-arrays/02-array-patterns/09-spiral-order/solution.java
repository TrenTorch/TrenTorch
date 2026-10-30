import java.util.Arrays;

public class Main {
    // O(m*n) time, O(m*n) space
    static long[] spiralOrder(long[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return new long[0];
        }
        int rows = matrix.length;
        int cols = matrix[0].length;
        long[] result = new long[rows * cols];
        int idx = 0;
        int top = 0, bottom = rows - 1, left = 0, right = cols - 1;
        while (top <= bottom && left <= right) {
            // top row
            for (int i = left; i <= right; i++) {
                result[idx++] = matrix[top][i];
            }
            // right column
            for (int i = top + 1; i <= bottom; i++) {
                result[idx++] = matrix[i][right];
            }
            // bottom row
            if (top < bottom) {
                for (int i = right - 1; i >= left; i--) {
                    result[idx++] = matrix[bottom][i];
                }
            }
            // left column
            if (left < right) {
                for (int i = bottom - 1; i >= top + 1; i--) {
                    result[idx++] = matrix[i][left];
                }
            }
            top++;
            bottom--;
            left++;
            right--;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(spiralOrder(new long[][]{new long[]{1L, 2L, 3L}, new long[]{4L, 5L, 6L}, new long[]{7L, 8L, 9L}})));
    }
}
