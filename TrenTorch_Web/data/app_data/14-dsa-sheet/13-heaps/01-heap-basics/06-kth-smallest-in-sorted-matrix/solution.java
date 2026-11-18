public class Main {
    // O((rows + cols) * log(max - min)) time, O(1) space
    static long kthSmallestMatrix(long[][] matrix, long k) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        long lo = matrix[0][0];
        long hi = matrix[rows - 1][cols - 1];
        while (lo < hi) {
            long mid = Math.floorDiv(lo + hi, 2L);
            if (countAtMost(matrix, rows, cols, mid) >= k) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    private static long countAtMost(long[][] matrix, int rows, int cols, long x) {
        long count = 0;
        int col = cols - 1;
        for (int r = 0; r < rows; r++) {
            while (col >= 0 && matrix[r][col] > x) {
                col--;
            }
            count += col + 1;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(kthSmallestMatrix(new long[][]{new long[]{1L, 5L, 9L}, new long[]{10L, 11L, 13L}, new long[]{12L, 13L, 15L}}, 8L));
    }
}
