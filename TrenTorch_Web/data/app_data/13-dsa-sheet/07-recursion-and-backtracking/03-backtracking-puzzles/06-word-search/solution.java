public class Main {
    // O(R * C * 4^L) time in the worst case (L = word length), O(R * C) space for the grid copy and recursion
    static boolean wordSearch(String[] board, String word) {
        if (word.isEmpty()) {
            return true;
        }
        int rows = board.length;
        char[][] grid = new char[rows][];
        for (int r = 0; r < rows; r++) {
            grid[r] = board[r].toCharArray();
        }
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < grid[r].length; c++) {
                if (wordGo(grid, word, r, c, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    static boolean wordGo(char[][] grid, String word, int r, int c, int i) {
        if (i == word.length()) {
            return true;
        }
        if (r < 0 || r >= grid.length || c < 0 || c >= grid[r].length || grid[r][c] != word.charAt(i)) {
            return false;
        }
        char saved = grid[r][c];
        grid[r][c] = '#';
        boolean found = wordGo(grid, word, r + 1, c, i + 1)
                || wordGo(grid, word, r - 1, c, i + 1)
                || wordGo(grid, word, r, c + 1, i + 1)
                || wordGo(grid, word, r, c - 1, i + 1);
        grid[r][c] = saved;
        return found;
    }

    public static void main(String[] args) {
        System.out.println(wordSearch(new String[]{"abce", "sfcs", "adee"}, "abcced"));
    }
}
