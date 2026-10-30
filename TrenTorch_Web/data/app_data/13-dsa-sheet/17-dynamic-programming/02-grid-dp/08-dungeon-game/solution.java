public class Main {
    // O(m*n) time, O(n) space where m=rows, n=cols
    static long calculateMinimumHp(long[][] dungeon) {
        int rows = dungeon.length;
        int cols = rows > 0 ? dungeon[0].length : 0;
        if (rows == 0 || cols == 0) {
            return 1;
        }
        long INF = 1_000_000_000L;
        long[] need = new long[cols + 1];
        for (int i = 0; i <= cols; i++) {
            need[i] = INF;
        }
        need[cols - 1] = 1;
        for (int r = rows - 1; r >= 0; r--) {
            for (int c = cols - 1; c >= 0; c--) {
                long bestNext = Math.min(need[c], need[c + 1]);
                if (r == rows - 1 && c == cols - 1) {
                    bestNext = 1;
                }
                need[c] = Math.max(1, bestNext - dungeon[r][c]);
            }
            need[cols] = INF;
        }
        return need[0];
    }

    public static void main(String[] args) {
        System.out.println(calculateMinimumHp(new long[][]{new long[]{-2L, -3L, 3L}, new long[]{-5L, -10L, 1L}, new long[]{10L, 30L, -5L}}));
    }
}
