import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(m*n) time, O(m+n) space
    static long[][] setMatrixZeroes(long[][] matrix) {
        int rows = matrix.length;
        if (rows == 0) return new long[0][];
        int cols = matrix[0].length;
        Set<Integer> zeroRows = new HashSet<>();
        Set<Integer> zeroCols = new HashSet<>();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == 0) {
                    zeroRows.add(i);
                    zeroCols.add(j);
                }
            }
        }
        long[][] result = new long[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (zeroRows.contains(i) || zeroCols.contains(j)) {
                    result[i][j] = 0;
                } else {
                    result[i][j] = matrix[i][j];
                }
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(setMatrixZeroes(new long[][]{new long[]{1L, 2L, 3L}, new long[]{4L, 0L, 6L}, new long[]{7L, 8L, 9L}})));
    }
}
