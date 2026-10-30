import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

public class Main {
    // O(n * 2^n) time, O(n^2) space
    static String[][] palindromePartitions(String s) {
        int n = s.length();
        if (n == 0) {
            return new String[][] { new String[0] };
        }
        boolean[][] pal = new boolean[n][n];
        for (int len = 1; len <= n; len++) {
            for (int i = 0; i + len <= n; i++) {
                int j = i + len - 1;
                pal[i][j] = s.charAt(i) == s.charAt(j) && (len <= 2 || pal[i + 1][j - 1]);
            }
        }
        List<List<String>> result = new ArrayList<>();
        backtrack(s, pal, 0, new ArrayList<>(), result);
        String[][] ans = new String[result.size()][];
        for (int i = 0; i < result.size(); i++) {
            ans[i] = result.get(i).toArray(new String[0]);
        }
        return ans;
    }

    private static void backtrack(String s, boolean[][] pal, int start, List<String> current, List<List<String>> result) {
        if (start == s.length()) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int j = start; j < s.length(); j++) {
            if (pal[start][j]) {
                current.add(s.substring(start, j + 1));
                backtrack(s, pal, j + 1, current, result);
                current.remove(current.size() - 1);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(palindromePartitions("aab")));
    }
}
