public class Main {
    // O(n + m) time, O(m) space (KMP automaton-style scan)
    static long countOverlapping(String text, String pattern) {
        int m = pattern.length();
        int[] fail = new int[m];
        int k = 0;
        for (int i = 1; i < m; i++) {
            while (k > 0 && pattern.charAt(i) != pattern.charAt(k)) {
                k = fail[k - 1];
            }
            if (pattern.charAt(i) == pattern.charAt(k)) {
                k++;
            }
            fail[i] = k;
        }
        long count = 0;
        k = 0;
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            while (k > 0 && ch != pattern.charAt(k)) {
                k = fail[k - 1];
            }
            if (ch == pattern.charAt(k)) {
                k++;
            }
            if (k == m) {
                count++;
                k = fail[k - 1];
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countOverlapping("aaaa", "aa"));
    }
}
