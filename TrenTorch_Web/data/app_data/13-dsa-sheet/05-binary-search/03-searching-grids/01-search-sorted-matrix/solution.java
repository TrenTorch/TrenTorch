public class Main {
    // O(log(rows*cols)) time, O(1) space
    static boolean searchMatrix(long[][] matrix, long target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return false;
        }
        int rows = matrix.length;
        int cols = matrix[0].length;
        int lo = 0;
        int hi = rows * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int row = mid / cols;
            int col = mid % cols;
            long value = matrix[row][col];
            if (value == target) {
                return true;
            } else if (value < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(searchMatrix(new long[][]{new long[]{1L, 3L, 5L, 7L}, new long[]{10L, 11L, 16L, 20L}, new long[]{23L, 30L, 34L, 60L}}, 3L));
    }
}
