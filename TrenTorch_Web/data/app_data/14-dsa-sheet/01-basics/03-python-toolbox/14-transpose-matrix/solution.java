public class Main {
    // O(rows*cols) time, O(rows*cols) space
    static long[][] transposeMatrix(long[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return new long[0][];
        }
        int rows = matrix.length;
        int cols = matrix[0].length;
        long[][] result = new long[cols][rows];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[j][i] = matrix[i][j];
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(transposeMatrix(new long[][]{new long[]{1L, 2L, 3L}, new long[]{4L, 5L, 6L}})));
    }
}
