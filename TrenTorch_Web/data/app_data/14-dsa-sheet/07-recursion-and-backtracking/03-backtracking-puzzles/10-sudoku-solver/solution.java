import java.util.*;

public class Main {
    // Backtracking with most-constrained-cell choice: exponential worst case, O(81 * 9) space
    static long[][] sudokuSolver(long[][] board) {
        long[][] grid = new long[9][9];
        boolean[][] rowUsed = new boolean[9][10];
        boolean[][] colUsed = new boolean[9][10];
        boolean[][] boxUsed = new boolean[9][10];
        List<int[]> empty = new ArrayList<>();
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                grid[r][c] = board[r][c];
                int v = (int) board[r][c];
                if (v != 0) {
                    rowUsed[r][v] = true;
                    colUsed[c][v] = true;
                    boxUsed[r / 3 * 3 + c / 3][v] = true;
                } else {
                    empty.add(new int[]{r, c});
                }
            }
        }
        solveSudoku(grid, rowUsed, colUsed, boxUsed, empty);
        return grid;
    }

    static List<Integer> sudokuCandidates(boolean[][] rowUsed, boolean[][] colUsed, boolean[][] boxUsed, int r, int c) {
        List<Integer> options = new ArrayList<>();
        int box = r / 3 * 3 + c / 3;
        for (int v = 1; v <= 9; v++) {
            if (!rowUsed[r][v] && !colUsed[c][v] && !boxUsed[box][v]) {
                options.add(v);
            }
        }
        return options;
    }

    static boolean solveSudoku(long[][] grid, boolean[][] rowUsed, boolean[][] colUsed,
                               boolean[][] boxUsed, List<int[]> empty) {
        int bestR = -1;
        int bestC = -1;
        List<Integer> bestOptions = null;
        for (int[] cell : empty) {
            int r = cell[0];
            int c = cell[1];
            if (grid[r][c] == 0) {
                List<Integer> options = sudokuCandidates(rowUsed, colUsed, boxUsed, r, c);
                if (bestOptions == null || options.size() < bestOptions.size()) {
                    bestR = r;
                    bestC = c;
                    bestOptions = options;
                    if (options.size() <= 1) {
                        break;
                    }
                }
            }
        }
        if (bestOptions == null) {
            return true;
        }
        int box = bestR / 3 * 3 + bestC / 3;
        for (int v : bestOptions) {
            grid[bestR][bestC] = v;
            rowUsed[bestR][v] = true;
            colUsed[bestC][v] = true;
            boxUsed[box][v] = true;
            if (solveSudoku(grid, rowUsed, colUsed, boxUsed, empty)) {
                return true;
            }
            grid[bestR][bestC] = 0;
            rowUsed[bestR][v] = false;
            colUsed[bestC][v] = false;
            boxUsed[box][v] = false;
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(sudokuSolver(new long[][]{
                new long[]{5L, 3L, 0L, 0L, 7L, 0L, 0L, 0L, 0L},
                new long[]{6L, 0L, 0L, 1L, 9L, 5L, 0L, 0L, 0L},
                new long[]{0L, 9L, 8L, 0L, 0L, 0L, 0L, 6L, 0L},
                new long[]{8L, 0L, 0L, 0L, 6L, 0L, 0L, 0L, 3L},
                new long[]{4L, 0L, 0L, 8L, 0L, 3L, 0L, 0L, 1L},
                new long[]{7L, 0L, 0L, 0L, 2L, 0L, 0L, 0L, 6L},
                new long[]{0L, 6L, 0L, 0L, 0L, 0L, 2L, 8L, 0L},
                new long[]{0L, 0L, 0L, 4L, 1L, 9L, 0L, 0L, 5L},
                new long[]{0L, 0L, 0L, 0L, 8L, 0L, 0L, 7L, 9L}})));
    }
}
