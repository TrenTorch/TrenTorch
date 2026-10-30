public class Main {
    // O(n*m) time, O(m) space where n = s.length(), m = p.length()
    static boolean isMatchRegex(String s, String p) {
        int n = s.length();
        int m = p.length();
        boolean[] prev = new boolean[m + 1];
        prev[0] = true;
        for (int j = 2; j <= m; j++) {
            if (p.charAt(j - 1) == '*') {
                prev[j] = prev[j - 2];
            }
        }
        for (int i = 1; i <= n; i++) {
            boolean[] cur = new boolean[m + 1];
            for (int j = 1; j <= m; j++) {
                if (p.charAt(j - 1) == '*') {
                    cur[j] = cur[j - 2] || (fits(p.charAt(j - 2), s.charAt(i - 1)) && prev[j]);
                } else {
                    cur[j] = fits(p.charAt(j - 1), s.charAt(i - 1)) && prev[j - 1];
                }
            }
            prev = cur;
        }
        return prev[m];
    }

    private static boolean fits(char pc, char sc) {
        return pc == '.' || pc == sc;
    }

    public static void main(String[] args) {
        System.out.println(isMatchRegex("aab", "c*a*b"));
    }
}
