import java.util.*;

public class Main {
    static class TrieNode {
        Map<Character, TrieNode> next = new HashMap<>();
        String word;
    }

    // O(R * C * 4^L) worst case, pruned by the trie; O(total word length) space
    static String[] findWords(String[] board, String[] words) {
        int rows = board.length;
        int cols = rows > 0 ? board[0].length() : 0;
        TrieNode trie = new TrieNode();
        for (String word : words) {
            TrieNode node = trie;
            for (int i = 0; i < word.length(); i++) {
                node = node.next.computeIfAbsent(word.charAt(i), k -> new TrieNode());
            }
            node.word = word;
        }
        char[][] grid = new char[rows][];
        for (int r = 0; r < rows; r++) {
            grid[r] = board[r].toCharArray();
        }
        Set<String> found = new HashSet<>();
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dfs(grid, rows, cols, r, c, trie, found);
            }
        }
        List<String> sorted = new ArrayList<>(found);
        Collections.sort(sorted);
        return sorted.toArray(new String[0]);
    }

    static void dfs(char[][] grid, int rows, int cols, int r, int c, TrieNode node, Set<String> found) {
        char ch = grid[r][c];
        TrieNode nxt = node.next.get(ch);
        if (nxt == null) {
            return;
        }
        if (nxt.word != null) {
            found.add(nxt.word);
        }
        grid[r][c] = '#';
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != '#') {
                dfs(grid, rows, cols, nr, nc, nxt, found);
            }
        }
        grid[r][c] = ch;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(findWords(new String[]{"oaan", "etae", "ihkr", "iflv"}, new String[]{"oath", "pea", "eat", "rain"})));
    }
}
