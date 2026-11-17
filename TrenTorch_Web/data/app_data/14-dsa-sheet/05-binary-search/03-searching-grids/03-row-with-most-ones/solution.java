public class Main {
    // O(rows + cols) time, O(1) space
    static long rowWithMostOnes(long[][] matrix) {
        if (matrix == null || matrix.length == 0) return -1;
        int col = matrix[0].length;
        long bestRow = -1;
        for (int i = 0; i < matrix.length; i++) {
            boolean moved = false;
            while (col > 0 && matrix[i][col - 1] == 1L) {
                col--;
                moved = true;
            }
            if (moved) {
                bestRow = i;
            }
        }
        return bestRow;
    }

    public static void main(String[] args) {
        System.out.println(rowWithMostOnes(new long[][]{new long[]{0L, 0L, 1L, 1L}, new long[]{0L, 1L, 1L, 1L}, new long[]{0L, 0L, 0L, 1L}}));
    }
}
