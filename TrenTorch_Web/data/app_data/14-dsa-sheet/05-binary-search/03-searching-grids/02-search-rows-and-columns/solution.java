public class Main {
    // O((rows + cols) log(max(rows, cols))) time, O(log(max(rows, cols))) space
    static boolean searchMatrixIi(long[][] matrix, long target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return false;
        }
        return search(matrix, target, 0, matrix.length - 1, 0, matrix[0].length - 1);
    }

    private static boolean search(long[][] matrix, long target, int r0, int r1, int c0, int c1) {
        if (r0 > r1 || c0 > c1) {
            return false;
        }
        if (r1 - r0 <= c1 - c0) {
            int r = (r0 + r1) / 2;
            int lo = c0;
            int hi = c1 + 1;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (matrix[r][mid] < target) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            if (lo <= c1 && matrix[r][lo] == target) {
                return true;
            }
            return search(matrix, target, r0, r - 1, lo, c1) ||
                   search(matrix, target, r + 1, r1, c0, lo - 1);
        } else {
            int c = (c0 + c1) / 2;
            int lo = r0;
            int hi = r1 + 1;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (matrix[mid][c] < target) {
                    lo = mid + 1;
                } else {
                    hi = mid;
                }
            }
            if (lo <= r1 && matrix[lo][c] == target) {
                return true;
            }
            return search(matrix, target, r0, lo - 1, c + 1, c1) ||
                   search(matrix, target, lo, r1, c0, c - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(searchMatrixIi(new long[][]{new long[]{1L, 4L, 7L, 11L}, new long[]{2L, 5L, 8L, 12L}, new long[]{3L, 6L, 9L, 16L}, new long[]{10L, 13L, 14L, 17L}}, 5L));
    }
}
