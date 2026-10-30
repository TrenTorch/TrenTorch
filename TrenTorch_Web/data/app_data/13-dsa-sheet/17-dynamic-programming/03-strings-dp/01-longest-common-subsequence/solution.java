public class Main {
    // O(n*m) time, O(min(n,m)) space
    static long lcsLength(String a, String b) {
        if (b.length() > a.length()) {
            String temp = a;
            a = b;
            b = temp;
        }
        int m = a.length();
        int n = b.length();
        int[] prev = new int[n + 1];
        for (int i = 1; i <= m; i++) {
            int[] cur = new int[n + 1];
            for (int j = 1; j <= n; j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    cur[j] = prev[j - 1] + 1;
                } else {
                    cur[j] = Math.max(prev[j], cur[j - 1]);
                }
            }
            prev = cur;
        }
        return prev[n];
    }

    public static void main(String[] args) {
        System.out.println(lcsLength("abcde", "ace"));
    }
}
