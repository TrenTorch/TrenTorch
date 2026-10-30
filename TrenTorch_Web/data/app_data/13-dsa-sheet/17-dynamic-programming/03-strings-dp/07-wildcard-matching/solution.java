public class Main {
    // O(n*m) time, O(m) space where n = s.length(), m = p.length()
    static boolean isMatchWildcard(String s, String p) {
        int n = s.length();
        int m = p.length();
        boolean[] prev = new boolean[m + 1];
        prev[0] = true;
        for (int j = 1; j <= m; j++) {
            prev[j] = prev[j - 1] && p.charAt(j - 1) == '*';
        }
        for (int i = 1; i <= n; i++) {
            boolean[] cur = new boolean[m + 1];
            for (int j = 1; j <= m; j++) {
                char pc = p.charAt(j - 1);
                if (pc == '*') {
                    cur[j] = cur[j - 1] || prev[j];
                } else if (pc == '?' || pc == s.charAt(i - 1)) {
                    cur[j] = prev[j - 1];
                }
            }
            prev = cur;
        }
        return prev[m];
    }

    public static void main(String[] args) {
        System.out.println(isMatchWildcard("aa", "*"));
    }
}
