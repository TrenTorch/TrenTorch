import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(1) time (fixed 9x9 board), O(1) space
    static boolean validSudoku(long[][] board) {
        Set<String> seen = new HashSet<>();
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                long digit = board[r][c];
                if (digit == 0) {
                    continue;
                }
                String[] keys = {
                    "row," + r + "," + digit,
                    "col," + c + "," + digit,
                    "box," + ((r / 3) * 3 + c / 3) + "," + digit
                };
                for (String key : keys) {
                    if (seen.contains(key)) {
                        return false;
                    }
                }
                seen.addAll(Arrays.asList(keys));
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(validSudoku(new long[][]{new long[]{5L, 3L, 0L, 0L, 7L, 0L, 0L, 0L, 0L}, new long[]{6L, 0L, 0L, 1L, 9L, 5L, 0L, 0L, 0L}, new long[]{0L, 9L, 8L, 0L, 0L, 0L, 0L, 6L, 0L}, new long[]{8L, 0L, 0L, 0L, 6L, 0L, 0L, 0L, 3L}, new long[]{4L, 0L, 0L, 8L, 0L, 3L, 0L, 0L, 1L}, new long[]{7L, 0L, 0L, 0L, 2L, 0L, 0L, 0L, 6L}, new long[]{0L, 6L, 0L, 0L, 0L, 0L, 2L, 8L, 0L}, new long[]{0L, 0L, 0L, 4L, 1L, 9L, 0L, 0L, 5L}, new long[]{0L, 0L, 0L, 0L, 8L, 0L, 0L, 7L, 9L}}));
    }
}
