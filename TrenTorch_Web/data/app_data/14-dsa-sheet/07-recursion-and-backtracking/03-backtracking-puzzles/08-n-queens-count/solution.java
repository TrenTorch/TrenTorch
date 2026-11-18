public class Main {
    // O(n!) time in the worst case with pruning, O(n) space for the column and diagonal marks
    static long nQueensCount(long n) {
        int size = (int) n;
        return queensGo(0, size, new boolean[size], new boolean[2 * size], new boolean[2 * size]);
    }

    static long queensGo(int r, int n, boolean[] cols, boolean[] diag1, boolean[] diag2) {
        if (r == n) {
            return 1;
        }
        long total = 0;
        for (int c = 0; c < n; c++) {
            int d1 = r - c + n - 1;
            int d2 = r + c;
            if (cols[c] || diag1[d1] || diag2[d2]) {
                continue;
            }
            cols[c] = true;
            diag1[d1] = true;
            diag2[d2] = true;
            total += queensGo(r + 1, n, cols, diag1, diag2);
            cols[c] = false;
            diag1[d1] = false;
            diag2[d2] = false;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(nQueensCount(4L));
    }
}
